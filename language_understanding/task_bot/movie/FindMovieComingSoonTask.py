#!/usr/bin/python
# -*- coding: utf-8 -*-

from dialog.Event import Event
from dialog.Parameter import Parameter
from dialog.Task import Task
from dialog.Context import *
from dialog.Event import Event

class FindMovieComingSoonTask(Task):
    def __init__(self):
        pass
    
    @staticmethod
    def Trigger(sess):
        if Event.IsIntentIs('find_movie_coming_soon', sess):
            return FindMovieComingSoonTask()
        return None

    def Run(self):
        sess = (yield)
        turn = sess.GetTurn(-1)
        if turn.intent == 'find_movie_coming_soon':
            movies = ['unforgettable']
            turn.agent_response = "find a movie. %s" % ",".join(movies)
            ctx = Context('movie_list', movies)
            ctx.SetExpireByTurn(1, sess)
            self.output_contexts = [ctx]
            return

