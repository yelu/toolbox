#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint

class Resolver(object):
    def __init__(self,
                 resolve_functor = None,
                 ):
        self.lu_value = None
        self.resolve_functor = resolve_functor
        if self.resolve_functor == None:
            self.resolve_functor = lambda x:Resolver.DefaultResolveFunctor(x)

    def Resolve(self):
        if self.resolve_functor == None:
            raise Exception("prompt for value collector not set")
        return self.resolve_functor(self.lu_value)

    @staticmethod
    def DefaultResolveFunctor(lu_value):
        if lu_value == None:
            return None
        for k, v in lu_value.items():
            if v is not None:
                return [v]
        return None 
            