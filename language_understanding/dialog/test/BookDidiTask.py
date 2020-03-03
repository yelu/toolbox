#!/usr/bin/python
# -*- coding: utf-8 -*-

from dialog.Event import Event
from dialog.Parameter import Parameter
from dialog.Task import Task

class BookDidiTask(Task):
    def __init__(self):
        self.param_time = Parameter('time')
        self.param_time.prompts = ['when will you go?']
        self.param_is_sharing = Parameter('is_sharing')
        self.param_is_sharing.prompts = ['would you like to share a car with other people?']
        self.param_seat_num = Parameter("seat_num")
        self.param_seat_num.prompts = ['how many seats do you want?']
        self.state = None
    
    @staticmethod
    def Trigger(s):
        pre_turn = s.GetTurn(-2)
        cur_turn = s.GetTurn(-1)
        if cur_turn and cur_turn.intent == 'book_didi':
            if not pre_turn: return BookDidiTask()
            if pre_turn.intent != 'book_didi' and \
               pre_turn.intent != 'is_confirm_is_sharing_yes' and \
               pre_turn.intent != 'is_confirm_is_sharing_no' and \
               pre_turn.intent != 'is_confirm_price_yes' and \
               pre_turn.intent != 'is_confirm_price_no':
                return BookDidiTask()
        return None

    def Run(self):
        while True:
            sess = (yield)
            self._FillParameter(sess)
            last_intent = sess.GetTurn(-1).intent
            if last_intent == 'book_didi':
                sess.next_prompt = self._GetNextPrmopt()
            elif last_intent == 'confirm_is_sharing_yes':
                if self.state == "confirm_is_sharing":
                    self.param_is_sharing.Set(True)
                    sess.next_prompt = self._GetNextPrmopt()
            elif last_intent == 'confirm_is_sharing_no':
                if self.state == "confirm_is_sharing":
                    self.param_is_sharing.Set(False)
                    sess.next_prompt = self._GetNextPrmopt()
            elif last_intent == 'confirm_price_yes':
                if self.state == "confirm_price":
                    sess.GetTurn(-1).agent_response = "ok. car reserved."
                    return
                else:
                    sess.next_prompt = self._GetNextPrmopt()
            elif last_intent == 'confirm_price_no':
                if self.state == "confirm_price":
                    sess.GetTurn(-1).agent_response = "ok. I canceled it."
                sess.next_prompt = self._GetNextPrmopt()

    def _FillParameter(self, sess):
        turn = sess.GetTurn(-1)
        for slot, v in turn.slots:
            if slot == "time":
                self.param_time.Set(v)
            elif slot == 'is_sharing':
                self.param_is_sharing.Set(v)
            elif slot == 'seat_num':
                self.param_seat_num.Set(v)
    
    def _GetNextPrmopt(self):
        time = self.param_time.Get()
        if time == None:
            self.state = None
            return self.param_time.prompts[0]
        if time != 'now':
            prompt = ("ok. I will reserve a car for you at %s. "
                      "The price is about 20 yuan. Do you confirm?") % (time,)
            self.state = "confirm_price"
            return prompt
        is_sharing = self.param_is_sharing.Get()
        if is_sharing == None:
            prompt = self.param_is_sharing.prompts[0]
            self.state = "confirm_is_sharing"
            return prompt
        if is_sharing:
            seat_num = self.param_seat_num.Get()
            if seat_num == None:
                self.state = None
                return self.param_seat_num.prompts[0]
            prompt = ("ok. I will reserve a car with %s seats. "
                      "The price is about 15 yuan. Do you confirm?") % (seat_num,)
            self.state = "confirm_price"
            return prompt
        else:
            prompt = ("ok. I will book a car with for you. "
                      "The price is about 20 yuan. Do you confirm?")
            self.state = "confirm_price"
            return prompt

