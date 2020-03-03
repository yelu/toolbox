#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint

class ValueCollector(object):
    def __init__(self,
                 prompt_functor = None,
                 prompts = None, 
                 ):
        self.prompt_functor = prompt_functor
        if self.prompt_functor == None:
            self.prompt_functor = lambda :ValueCollector.RandomPromptFuntor(prompts)

    def GetPrompt(self):
        if self.prompt_functor == None:
            raise Exception("prompt for value collector not set")
        return self.prompt_functor()

    @staticmethod
    def RandomPromptFuntor(prompts):
        return prompts[randint(0, len(prompts) - 1)]

            