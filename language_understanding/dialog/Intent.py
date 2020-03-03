#!/usr/bin/python
# -*- coding: utf-8 -*-

from Event import Event

class Intent(object):
    
    def __init__(self, ctx):
        self._value = None
        self._ctx = ctx
        
    def Set(self, v):
        self.state = "filled"
        if self.timeout == None or self.time_remaining >= 0: 
            self.value = v

    def get(self):
        if self.timeout != None:
            self.time_remaining = self.timeout
        if self.value == None:
            missing_params = set([self.name])
            raise ParameterMissingException(missing_params)
        return self.value

    def set_expire(self, ttl):
        self.ttl = ttl
