#!/usr/bin/python
# -*- coding: utf-8 -*-

from ..Session import *
from BookDidiTask import BookDidiTask
import unittest

if __name__ == '__main__':

    sess = Session()
    ctx_man = Conte
    sess.AddTaskTrigger(lambda : BookDidiTask.Trigger(sess))

    turn = Turn()

    turn.intent = 'book_didi'
    turn.user_query = 'go right now'
    turn.slots = [('time', 'now')]
    sess.AddTurn(turn)
    print (turn.prompt, turn.user_query, turn.agent_response)

    turn.intent = 'confirm_is_sharing_yes'
    turn.user_query = 'yes'
    sess.AddTurn(turn)
    print (turn.prompt, turn.user_query, turn.agent_response)
       
    turn.intent = 'book_didi'
    turn.user_query = 'go at 10:00 am'
    turn.slots = [('time', '10:00 am')]
    sess.AddTurn(turn)
    print (turn.prompt, turn.user_query, turn.agent_response)

    turn.intent = 'book_didi'
    turn.user_query = 'go right now'
    turn.slots = [('time', 'now')]
    sess.AddTurn(turn)
    print (turn.prompt, turn.user_query, turn.agent_response)

    turn.intent = 'confirm_is_sharing_yes'
    turn.user_query = 'yes'
    sess.AddTurn(turn)
    print (turn.prompt, turn.user_query, turn.agent_response)
       
    turn.intent = 'book_didi'
    turn.user_query = 'i want 2 seats'
    turn.slots = [('seat_num', '2')]
    sess.AddTurn(turn)
    print (turn.prompt, turn.user_query, turn.agent_response)

    turn.intent = 'confirm_price_yes'
    turn.user_query = 'confirm'
    sess.AddTurn(turn)
    print (turn.prompt, turn.user_query, turn.agent_response)

