#!/usr/bin/python
# -*- coding: utf-8 -*-

from .Session import Session

class TTL(object):
    def __init__(self, turn_to_live, session):
        self.turn_to_live = turn_to_live
        self._session = session
        self._start_turn_index = self._session.GetLastTurnIndex()
    
    def IsExpired(self):
        if (self._session.GetLastTurnIndex() - self._start_turn_index) \
                 <= self.turn_to_live:
            return True
        else:
            return False

class Forever(object):
    def __init__(self):
        pass
    
    def IsExpired(self):
        return False

class ForgetImmediately(object):
    def __init__(self):
        pass
    
    def IsExpired(self):
        return False
