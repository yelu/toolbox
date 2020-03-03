#!/usr/bin/python
# -*- coding: utf-8 -*-

import heapq
import json
from .Parameter import Parameter
from .Lifetime import *

class UnresolvedContextException(Exception):
    def __init__(self, contexts, message = None):
        self.contexts = contexts
        self.message = message

class Context(object):
    def __init__(self):
        self._parameters = {}
    
    def ToJson(self):
        dic = {}
        for param_name, param in self._parameters.items():
            dic[param_name] = {"name":param.name, "state":param.state,
                               "lu_value":param.lu_value,
                               "lu_value_latest":param.lu_value_latest,
                               "resolved_value":param.resolved_value
                               }
        return json.dumps(dic)

    def Add(self, param):
        self._parameters[param.name] = param
        return self

    def ForceForget(self, name):
        if name not in self._parameters:
            return
        self._parameters[name] = ForgetImmediately()
        del self._parameters[name]
    
    def Get(self, name):
        if name not in self._parameters:
            raise Exception("unregistered parameter \"%s\"" % name)
        context = self._parameters[name]
        if context.IsExpired():
            self.ForceForget(name)
        return context
    
    def AddDependency(self, a, b):
        """ a depends on b
        """
        param_a = self._parameters[a]
        param_a.dependent_params.add(b)
        param_a.dependent_param_values[a] = None
         
    def Disable(self, context):
        self._parameters[context].Disable()
    
    def Enable(self, context):
        self._parameters[context].Disable()
    
    def TopologicalSort(self, priority = None):
        dependency_graph = dict.fromkeys(self._parameters, set())
        for param_name, param in self._parameters.items():
            for dst_param_name in param.dependent_params:
                dependency_graph[dst_param_name].add(param_name)

        # get dependencies map
        in_degrees = dict.fromkeys(dependency_graph, 0)
        for src, dsts in dependency_graph.items():
            for dst in dsts:
                in_degrees[dst] += 1

        res = []
        while len(in_degrees) != 0:
            nxt = None
            if priority in in_degrees and in_degrees[priority] == 0:
                nxt = priority
            else:
                pq = [(k, v) for k, v in in_degrees.items()]
                pq = sorted(pq, key = lambda d:d[1])
                if pq[0][1] != 0:
                    raise Exception("circular dependency in graph")
                nxt = pq[0][0]
            del in_degrees[nxt]
            for dst in dependency_graph[nxt]:
                in_degrees[dst] -= 1
            res.append(nxt)
        
        return res