#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Game(object):
    #template_name = ''

    def make_question(self, *args, **kwargs):
        query = {'suma': '2+3'}
        response = {'suma': 5}
        return query, response

    def score(self, response, user_answer):
        r_suma = response.get('suma')
        u_suma = user_answer.get('suma', None)
        if isinstance(u_suma, int) and r_suma == int(u_suma):
            return 1
        else:
            return 0
