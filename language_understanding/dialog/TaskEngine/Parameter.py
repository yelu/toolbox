#!/usr/bin/python
# -*- coding: utf-8 -*-

from .DialogResponse import *
import json
from .Lifetime import *

default_lifetime = Forever()

class ResolveState(object):
    NotStart = "NotStart"
    PromptForValue = "PromptForValue"
    PromptForSelection = "PromptForSelection"
    Selction = "CheckSelection"
    Resolved = "Resolved"

class Parameter(object):
    def __init__(self, name, 
                 watched_intents,
                 watched_slots,
                 init_value = None,
                 lifetime = default_lifetime           
                 ):
        
        self.name = name
        self.watched_intents = set(watched_intents)
        self.watched_slots = set(watched_slots)
        if self.watched_slots == None or len(self.watched_slots) == 0:
            raise Exception("no slots watched in parameter %s" % self.name)     
        self.lu_value = init_value
        self.lu_value_latest = init_value
        self.resolved_value = None
        self.dependent_params = set()
        self.dependent_param_values = {}
        self._lifetime = lifetime
        self._disabled = False
        self.state = ResolveState.NotStart
        self.value_collector = None
        self.option_selector = None
        self.resolver = None
        self.retry_cnt = 3
    
    def ToJson(self):
        dic = {"name":self.name, "state":self.state,
               "lu_value_latest":self.lu_value_latest,
               "resolved_value":self.resolved_value
               }
        return json.dumps(dic)
    
    def CheckDependencyChange(self, memory):
        if self.lu_value == None and self.lu_value_latest != None:
            return True
        if self.lu_value == None and self.lu_value_latest == None:
            return False
        for k, v in self.lu_value.items():
            if v != self.lu_value_latest[k]:
                return True

        for param_name, param_value in self.dependent_param_values.items():
            param_value_latest = memory.Get(param_name).resolved_value
            if param_value != param_value_latest:
                return True
        return False
          
    def Save(self, query, semantic_frame):
        """return a bool to indicate whether the value has changed

        reset lu value if there are watched slot values, otherwise, keep
        original value
        """
        intents = semantic_frame["Intents"]
        slots  = semantic_frame["Slots"]
        if self.watched_intents != None \
            and len(self.watched_intents) != 0 \
            and len(set(self.watched_intents).intersection(set(intents))) == 0:
            return
                
        intersect = set(self.watched_slots).intersection(set(slots))
        # reset all slots before updating
        if len(intersect) != 0:
            self.lu_value_latest = dict.fromkeys(self.watched_slots, None)       
            for slot_name in intersect:
                self.lu_value_latest[slot_name] = slots[slot_name]

    def IsEmptyLUValue(self):
        if self.lu_value == None:
            return True
        for k, v in self.lu_value.items():
            if v is not None:
                return False
        return True

    def Reset(self):
        self.retry_cnt = 0
        self.state = ResolveState.NotStart

    def Resolve(self, query, memory):
        if self.retry_cnt > 3:
            self.Reset()
            return (0, TextDialogResponse("ops, i don't understand. try again later"))
        
        if self.CheckDependencyChange(memory):
            self.Reset()
            self.lu_value = self.lu_value_latest
            
        if self.state == ResolveState.NotStart and self.value_collector != None and \
            not self.IsEmptyLUValue():
            self.state = ResolveState.PromptForValue

        if self.state == ResolveState.NotStart:
            if self.value_collector == None and self.option_selector != None:
                self.state = ResolveState.PromptForSelection
                return (0, TextDialogResponse(self.option_selector.GetPrompt()))
            
            if self.value_collector != None:
                if self.IsEmptyLUValue():
                    self.state = ResolveState.PromptForValue
                    return (0, TextDialogResponse(self.value_collector.GetPrompt()))
        # in case of the following, we need to resolve the slot provided by user:
        # 1. prompt for value state
        # 2. has value collector and slot already
        elif self.state == ResolveState.PromptForValue or \
                (self.value_collector != None and \
                 self.state == ResolveState.NotStart and \
                 not self.IsEmptyLUValue()):
            # still need lu to tag the value as slot
            self.resolver.lu_value = self.lu_value
            
        elif self.state == ResolveState.PromptForSelection:
            # use query to understand directly
            selection = self.option_selector.Select(query)
            if selection != None:
                self.resolved_value = selection
                self.state = ResolveState.Resolved
                return (0, None)
            else:
                self.retry_cnt += 1
                return (0, TextDialogResponse(self.option_selector.GetPrompt()))
    
    def IsExpired(self):
        return self._lifetime.IsExpired()

    def Forget(self):
        self._lifetime = ForgetImmediately()
    
    def Disable(self):
        self._disabled = True
    
    def Enable(self):
        self._disabled = False
    
    def IsDisabled(self):
        return self._disabled

class IntentToSlot(object):
    def __init__(self, name, watched_intents, intents_mapping):
        self.name = name
        self.watched_intents = set(watched_intents)
        self.intents_mapping = intents_mapping
        self.value = {self.name:None}
    
    def Run(self, semantic_frame):
        intents = semantic_frame["Intents"]
        intersect = self.watched_intents.intersection(set(intents))
        # only update value when there are watched intents triggered.
        if len(intersect) == 0:        
            return semantic_frame
        # select one is enough, it is assumed all (triggered) intents
        # should have consistent mapping in each turn.
        self.value = {self.name : self.intents_mapping[list(intersect)[0]]}
        semantic_frame["Slots"].update(self.value)
        return semantic_frame

