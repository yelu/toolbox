#!/usr/bin/python
# -*- coding: utf-8 -*-

class OptionSelector(object):
    def __init__(self, 
                 prompt_functor = None,
                 options = None
                 ):
        self.options = options
        self.prompt_functor = prompt_functor
        if self.prompt_functor == None:
            self.prompt_functor = OptionSelector.DefaultTextPrompt
    
    def GetPrompt(self):
        if self.prompt_functor == None:
            raise Exception("prompt for option selector not set")
        return self.prompt_functor(self.options)

    @staticmethod
    def DefaultTextPrompt(options):
        res = "here are %d relevant mathches:\n%s\nwhich one do you prefer?" % \
              (len(options), \
               "\n".join(["%d. %s" % (i+1,x) for i,x in enumerate(options)]))
        return res

    def Select(self, selection):
        selection = selection.strip()
        if selection in self.options:
            return selection
        else:
            return None