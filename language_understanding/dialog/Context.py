#!/usr/bin/python
# -*- coding: utf-8 -*-

class Context(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def IsValid(self):
        if self.expiration_type == "ByTurn":
            if self._sess.GetTurnIndex() - self.start_turn_index <= self.turn_to_live:
                return True
            else:
                return False

    def SetExpireByTurn(self, turn_to_live, sess):
        self._sess = sess
        self.turn_to_live = turn_to_live
        self.start_turn_index = self._sess.GetTurnIndex()
        self.expiration_type = "ByTurn"

    def Renew(self):
        if self.expiration_type == "ByTurn":
            self.start_turn_index = self._sess.GetTurnIndex()

