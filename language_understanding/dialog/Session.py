#!/usr/bin/python
# -*- coding: utf-8 -*-

class Turn(object):
    def __init__(self):
        self.intent = None
        self.slots = []
        self.prompt = None
        self.user_query = None
        self.agent_response = None
        self.dialog_state = None

class Session(object):
    
    def __init__(self):
        self._turns = []
        self.next_prompt = None
        self._task_triggers = set()
        self._running_tasks = {}
        self._contexts = {}
        
    def AddTurn(self, turn):
        turn.prompt = self.next_prompt
        self._turns.append(turn)
        self._next_prompt = None

        # remove context that is expired.
        for ctx_name in self._contexts.keys():
            if not self._contexts[ctx_name].IsValid():
                del self._contexts[ctx_name]

        for tr in self._task_triggers:
            task = tr()
            if task:
                coro = task.Run()
                self._running_tasks[task] = coro
                next(coro)
        
        # Execute all tasks.
        completed_tasks = set()
        for t, coro in self._running_tasks.items():
            try:
                coro.send(self)
            except StopIteration as e:
                # Task.Run coroutine returns. Remove it from task lists.
                if t in self._running_tasks:
                    completed_tasks.add(t)
                # Add its output contexts if it has.
                if hasattr(t, "output_contexts"):
                    for c in t.output_contexts:
                        self.AddContext(c)
        for ele in completed_tasks:
            del self._running_tasks[ele]

    def GetTurn(self, idx):
        if idx >= len(self._turns) or idx < (0 - len(self._turns)):
            return None
        return self._turns[idx]

    def GetTurnIndex(self):
        return len(self._turns) - 1

    def AddEvent(self, event):
        self._events.add(event)

    def AddTaskTrigger(self, tr):
        self._task_triggers.add(tr)

    def RemoveTask(self, task):
        if task in self._running_tasks:
            del self._running_tasks[task]

    def AddContext(self, ctx):
        self._contexts[ctx.name] = ctx

    def GetContext(self, ctx_name):
        if ctx_name in self._contexts:
            self._contexts[ctx_name].Renew()
            return self._contexts[ctx_name]
        else:
            return None
