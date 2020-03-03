#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import json
from TaskEngine.Session import Session
from TaskEngine.Session import Turn
from TaskEngine.Memory import Memory
from TaskEngine.Parameter import *
from TaskEngine.Task import Task
from TaskEngine.ValueCollector import ValueCollector
from TaskEngine.OptionSelector import OptionSelector
from TaskEngine.Resolver import Resolver
from TaskEngine.ParamRanker import ParamRanker
import unittest

def LocationResolveFunctor(lu_slots):
    candidates = ["tiananmen square", "tiananmen west railway station"]
    return candidates

def ParamRankFunctor(memory):
    src, dst, time, is_sharing, seat_num = memory.Get("src"), memory.Get("dst"), \
                                           memory.Get("time"), memory.Get("is_sharing"), \
                                           memory.Get("seat_num")
    if src.resolved_value == None:
        return ["src"]
    if dst.resolved_value == None:
        return ["dst"]
    if time.resolved_value == None:
        return ["time"]

    if time.resolved_value != "now":
        return []
    if time.resolved_value == "now":
        return ["is_sharing"]
    if is_sharing.resolved_value == None:
        return ["is_sharing"]
    if is_sharing.resolved_value:
        return ["seat_num"]
    else:
        return []

    if seat_num.resolved_value == None:
        return ["seat_num"]

    return []

'''
    slot_value = None
    for k,v in lu_slots.items():
        if v is not None:
            slot_value = v
    if slot_value in candidates:
        return [slot_value]
    else:
        return candidates
'''

if __name__ == '__main__':

    session = Session()
    memory = Memory()

    src = Parameter(name = "src",
                    watched_intents = ['book_uber'],
                    watched_slots = ["src"],
                    init_value = None)
    src.resolver = Resolver(LocationResolveFunctor)
    src.value_collector = ValueCollector(prompts = ["where to pick you up?"]) 
    src.option_selector = OptionSelector()

    dst = Parameter(name = "dst",
                    watched_intents = ['book_uber'],
                    watched_slots = ["dst"],
                    init_value = None)
    dst.resolver = Resolver(LocationResolveFunctor)
    dst.value_collector = ValueCollector(prompts = ["where to go?"]) 
    dst.option_selector = OptionSelector()

    time = Parameter(name = "time", 
                   watched_intents = ['book_uber'],
                   watched_slots = ["time"],
                   init_value = None)
    time.resolver = Resolver()
    time.value_collector = ValueCollector(prompts = ["when do you want to leave?"])

    is_sharing = Parameter(name = "is_sharing", 
                           watched_intents = [],
                           watched_slots = ['is_sharing'],
                           init_value = None)
    intent_to_slot = IntentToSlot("is_sharing",
                                  watched_intents = ["is_sharing_yes", "is_sharing_no"],
                                  intents_mapping = {"is_sharing_yes":True, "is_sharing_no":False})
    is_sharing.resolver = Resolver()
    is_sharing.value_collector = ValueCollector(prompts = ["do you want to share a car with others?"])

    seat_num = Parameter(name = "seat_num", 
                         watched_intents = ['book_uber'],
                         watched_slots = ["seat_num"],
                         init_value = None)
    seat_num.resolver = Resolver()
    seat_num.value_collector = ValueCollector(prompts = ["how many seats?"])

    memory.Add(src).Add(dst).Add(time).Add(is_sharing).Add(seat_num)

    task = Task(session, memory, ['src', 'dst', 'time', 'is_sharing', 'seat_num'])
    task.param_ranker = ParamRanker(ParamRankFunctor)

    semantic_frame = {"Intents":[], "Slots":{}}
    semantic_frame = intent_to_slot.Run(semantic_frame)
    print(semantic_frame)
    res = task.Run("", semantic_frame)
    print(res.text)

    semantic_frame = {"Intents":['book_uber'], 
                      "Slots":{'dst':'tiananmen'}}
    semantic_frame = intent_to_slot.Run(semantic_frame)
    print(semantic_frame)
    res = task.Run("tiananmen", semantic_frame)
    print(res.text)

    semantic_frame = {"Intents":['book_uber'], 
                      "Slots":{'dst':'tiananmen square'}}
    semantic_frame = intent_to_slot.Run(semantic_frame)
    print(semantic_frame)
    res = task.Run("tiananmen square", semantic_frame)
    print(res.text)

    semantic_frame = {"Intents":['book_uber'], 
                      "Slots":{'time':'now'}}
    semantic_frame = intent_to_slot.Run(semantic_frame)
    print(semantic_frame)
    res = task.Run("tiananmen", semantic_frame)
    print(res.text)

    semantic_frame = {"Intents":['is_sharing_no'], 
                      "Slots":{}}
    semantic_frame = intent_to_slot.Run(semantic_frame)
    print(semantic_frame)
    res = task.Run("tiananmen", semantic_frame)
    print(res.text)

    semantic_frame = {"Intents":['book_uber'], 
                      "Slots":{'seat_num':'1'}}
    semantic_frame = intent_to_slot.Run(semantic_frame)
    print(semantic_frame)
    res = task.Run("tiananmen square", semantic_frame)
    print(res.text)

    semantic_frame = {"Intents":['book_uber'], 
                      "Slots":{'seat_num':'1'}}
    semantic_frame = intent_to_slot.Run(semantic_frame)
    print(semantic_frame)
    res = task.Run("tiananmen square", semantic_frame)
    print(res.text)
    