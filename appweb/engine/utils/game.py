#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        print(u"Query: %s" % question['query'])

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
        print(u"\t%s: %s" % (question['query'], question['options'][response['answer']]))

    def play_options(self, question):
        for i in range(len(question['options'])):
            i += 1
            print(u"\t%d) %s" % (i, question['options'][i-1]))
        user_input = input(u"\nIntroduce el número respuesta: ")
        user_answer = {'answer': int(user_input)-1}
        return user_answer