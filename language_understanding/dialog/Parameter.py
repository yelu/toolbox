#!/usr/bin/python
# -*- coding: utf-8 -*-

class Parameter(object):
    def __init__(self, name, state = "empty"):
        self.state = state
        self.prompts = []
        self.name = name        
        self._value = None

    def Set(self, v):
        self._value = v

    def Get(self):
        return self._value

