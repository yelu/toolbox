#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from .DialogResponse import *
from .Parameter import Parameter
from .Context import Context
from .Parameter import ResolveState
from .Lifetime import *

class Task(object):
    
    def __init__(self, session, context, params):
        self.session = session
        self.context = context
        self.params = set(params)
        self.semantic_frame = {"Intents":[],"Slots":{}}
        self.resolving_param = None
        self.param_ranker = None
               
    def Run(self, query, semantic_frame):
        # if a param is resolving and wait for selction, skip store lu results.
        if not (self.resolving_param and \
           self.resolving_param[1].state == ResolveState.PromptForSelection):
            for param in self.params:
                self.context.Get(param).Save(query, semantic_frame)
        
        # if there is a resolving param and we decide to stay on, continue to resolve it.
        # only update its related intents/slots.
        if self.resolving_param != None and self.ShouldStayOnCurParam():
            param_name, param = self.resolving_param
            res = param.Resolve(query, self.context)
            if param.state == ResolveState.Resolved:
                self.resolving_param = None            
            else:  # resolved.
                return res[1]

        # find next unresolved param and stop to resolve it
        for param_name in self.param_ranker.Rank(self.context):
            param = self.context.Get(param_name)
            self.resolving_param = (param_name, param)           
            res = param.Resolve(query, self.context)
            if param.state == ResolveState.Resolved:
                self.resolving_param = None            
            else:  # resolved.
                return res[1]

        # here all params resovled
        return TextDialogResponse("all done!")

    def ToJson(self):
        dic = {"resolving_param":None if self.resolving_param else self.resolving_param[0],
               }
        return json.dumps(dic)

    def ShouldStayOnCurParam(self):
        if self.resolving_param == None:
            return False
        if self.resolving_param[1].state == ResolveState.NotStart or \
           self.resolving_param[1].state == ResolveState.Resolved:
           return False
        return True

