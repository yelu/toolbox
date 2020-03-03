#!/usr/bin/python
# -*- coding: utf-8 -*-

from dialog.Event import Event
from dialog.Parameter import Parameter
from dialog.Task import Task
from dialog.Context import *
from dialog.Event import Event

class MovieFactTask(Task):
    def __init__(self):
        pass

    @staticmethod
    def Trigger(sess):
        if Event.IsIntentChangeTo('movie_fact_actor', sess):
            return MovieFactTask()
        else:
            return None

    def Run(self):
        while True:
            sess = (yield)
            turn = sess.GetTurn(-1)
            if turn.intent == 'movie_fact_actor':
                movie = self._FindSlot(turn.slots, "movie")
                if movie:
                    turn.agent_response = 'Robin williams acts in %s' % movie
                    return
                
                movie_list = sess.GetContext('movie_list').value
                print(movie_list)
                if not movie_list or len(movie_list) == 0:
                    sess.next_prompt = "which movie are you talking about?"
                    continue
                position = self._FindSlot(turn.slots, 'position')
                if not position:
                    sess.next_prompt = "which movie are you talking about?"
                    continue
                if position == 'first':
                    movie = movie_list[0]
                elif position == 'second' and len(movie_list) >= 2:
                    movie = movie_list[1]
                elif position == 'third' and len(movie_list) >= 3:
                    movie = movie_list[2]
                elif position == 'last':
                    movie = movie_list[-1]
            
                if movie:
                    turn.agent_response = 'Leonardo acts in %s' % movie
                else:
                    sess.next_prompt = "which movie are you talking about?"
            else:
                return
                
    def _FindSlot(self, slots, name):
        for k, v in slots:
            if k.strip().lower() == name and len(v.strip()) != 0:
                return v.strip()
        return None
