#!/usr/bin/python
# -*- coding: utf-8 -*-

class Event(object):
    
    def __init__(self):
        pass
    
    @staticmethod
    def IsIntentChangeTo(target_intent, sess):
        pre_turn = sess.GetTurn(-2)
        cur_turn = sess.GetTurn(-1)
        if cur_turn == None or cur_turn.intent == None:
            return False
        if cur_turn.intent == target_intent:
            if pre_turn == None or \
               pre_turn.intent == None or \
               pre_turn.intent != target_intent:
               return True
        return False

    @staticmethod
    def IsIntentIs(target_intent, sess):
        cur_turn = sess.GetTurn(-1)
        if cur_turn != None and \
           cur_turn.intent != None and \
           cur_turn.intent == target_intent:
                return True
        else:
            return False

    @staticmethod
    def IsIntentChangeFrom(source_intent, sess):
        pre_turn = self._sess.GetTurn(-2)
        cur_turn = self._sess.GetTurn(-1)
        if pre_turn == None or pre_turn.intent == None:
            return False
        if pre_turn.intent == source_intent:
            if cur_turn == None or \
               cur_turn.intent == None or \
               cur_turn.intent != source_intent:
                return True
        return False

