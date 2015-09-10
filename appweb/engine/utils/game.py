#!/usr/bin/env python
# -*- coding: utf-8 -*-

from builtins import input

class QuestionError(Exception):
    pass


class GameBase(object):
    title = None

    def __init__(self, *args, **kwargs):
        pass

    def play_config(self):
        return {}

    def play_interactive(self, rounds=1, *args, **kwargs):
        title = self.title or 'no-title'

        print("="*(4 + len(title)))
        print("= %s =" % title)
        print("="*(4 + len(title)))

        config = self.play_config()
        kwargs.update(**config)

        for _ in range(rounds):
            self.play_round(*args, **kwargs)

    def play_round(self, *args, **kwargs):
        question, response = self.make_question(*args, **kwargs)
        print("Query: %s" % question['query'])

        if 'options' in question:
            user_answer = self.play_options(question)
        elif 'yesno' in question:
            user_answer = self.play_yesno(question)
        else:
            raise NotImplementedError()

        score = self.score(response, user_answer)
        if score > 0:
            print("\t¡¡BIEN!! %f points" % score)
        else:
            print("\t¡mal!")
        print("\t%s" % response['info'])

    def play_options(self, question):
        for i in range(len(question['options'])):
            i += 1
            print("\t%d) %s" % (i, question['options'][i-1]))
        user_input = input("\nIntroduce el número de la respuesta: ")
        user_answer = {'answer': int(user_input)-1}
        return user_answer
