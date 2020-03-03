#!/usr/bin/python
# -*- coding: utf-8 -*-

class ParamRanker(object):
    def __init__(self, ranking_functor = None):
        self.ranking_functor = ranking_functor
        if self.ranking_functor == None:
            self.ranking_functor = ParamRanker.DefaultRankingFunctor
    
    def Rank(self, memory):
        return self.ranking_functor(memory)

    @staticmethod
    def DefaultRankingFunctor(memory):
        return memory.TopologicalSort()

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
