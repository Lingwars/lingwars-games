#!/usr/bin/env python
# -*- coding: utf-8 -*-

from engine.utils.game import GameBase

class Game(GameBase):
    title = 'Word 2 Def (simple)'

    def make_question(self, *args, **kwargs):
        query = '2+3'
        options = [1, 2, 3, 4, 5]

        question = {'query': query, 'options': options}
        response = {'answer': options.index(5), 'info': '2+3 = 5'}
        return question, response

    def score(self, response, user_answer):
        u = user_answer.get('answer', None)
        try:
            u = int(u)
        except TypeError:
            return 0
        else:
            return 1 if u == response.get('answer') else 0
