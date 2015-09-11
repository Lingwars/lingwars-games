#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from engine.utils.game import GameBase
from random import randint

try:
    from django.utils.translation import ugettext_lazy
except ImportError:
    ugettext_lazy = lambda u: u


class SumGame(GameBase):
    title = 'Maths: Sum'
    author = 'Lingwars'
    description = ugettext_lazy("""
    In this game you will be presented with two integers and you have to compute how much their sum is.
    """)

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
