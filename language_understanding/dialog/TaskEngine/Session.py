#!/usr/bin/python
# -*- coding: utf-8 -*-

class Turn(object):
    def __init__(self):
        self.intents = set()
        self.slots = {}
        self.dialog_prompt = []
        self.user_query = []
        self.dialog_response = []

class Session(object):
    
    def __init__(self):
        self.turns = []
        
    def AddTurn(self, turn):
        self.turns.append(turn)

    def GetTurn(self, idx):
        if idx >= len(self.turns) or idx < (0 - len(self.turns)):
            return None
        return self._turns[idx]

    def GetLastTurnIndex(self):
        return len(self._turns) - 1
