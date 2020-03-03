#!/usr/bin/python
# -*- coding: utf-8 -*-

from dialog.Event import Event
from dialog.Parameter import Parameter
from dialog.Task import Task
from dialog.Context import *

class FindMovieInTheaterTask(Task):
    def __init__(self):
        pass
    
    @staticmethod
    def Trigger(sess):
        if Event.IsIntentIs('find_movie_in_theater', sess):
            return FindMovieInTheaterTask()
        else:
            return None

    def Run(self):
        sess = (yield)
        turn = sess.GetTurn(-1)
        if turn.intent == 'find_movie_in_theater':
            movies = ['x man', 'perception']
            ctx = Context('movie_list', movies)
            turn.agent_response = "find 2 movies. %s" % ",".join(movies)
            ctx.SetExpireByTurn(1, sess)
            self.output_contexts = [ctx]
            return

