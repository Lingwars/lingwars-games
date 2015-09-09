#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from engine.utils.game import GameBase
from random import randint


class SumGame(GameBase):
    title = 'Maths: Sum'

    def make_question(self, *args, **kwargs):
        a = randint(0, 100)
        b = randint(0, 100)

        query = "%d + %d" % (a, b)
        options = [a+b] + [randint(0, 200) for _ in range(4)]
        options = list(set(options)) # Delete duplicates

        question = {'query': query, 'options': options}
        response = {'answer': options.index(a+b), 'info': '%s = %d' % (query, a+b)}
        return question, response

    def score(self, response, user_answer):
        u = user_answer.get('answer', None)
        try:
            u = int(u)
        except TypeError:
            return 0
        else:
            return 1 if u == response.get('answer') else 0

game = SumGame()