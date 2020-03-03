#!/usr/bin/python
# -*- coding: utf-8 -*-

from dialog.Session import Session
from dialog.Session import Turn
from FindMovieInTheaterTask import FindMovieInTheaterTask
from FindMovieComingSoonTask import FindMovieComingSoonTask
from MovieFactTask import MovieFactTask
from intent.IntentCNN import IntentCNN
from slot.SlotLCCRF import SlotLCCRF
import json
import unittest

if __name__ == '__main__':

    sess = Session()
    
    sess.AddTaskTrigger(lambda : FindMovieInTheaterTask.Trigger(sess))
    sess.AddTaskTrigger(lambda : FindMovieComingSoonTask.Trigger(sess))
    sess.AddTaskTrigger(lambda : MovieFactTask.Trigger(sess))

    intent_cnn = IntentCNN()
    intent_cnn.Load('./intent_output/model/model.ckpt')

    slot_lccrf = SlotLCCRF()
    slot_lccrf.Load('./slot_output/model/')

    qs = ['find a movie in theater',
          'find a movie comming soon',
          'find a movie in theater',
          'who act in the first one',
          'who act in the last one',
          'who act in the second one']

    for q in qs:
        query = q.strip()
        if len(query) == 0:
            continue
        turn = Turn()
        turn.user_query = query
        turn.intent = intent_cnn.Predict(query)[0]
        turn.slots = slot_lccrf.Predict(query)
        print("intent:%s, slots:%s" % (turn.intent, json.dumps(turn.slots)))
        sess.AddTurn(turn)
        print((turn.prompt, turn.user_query, turn.agent_response))

