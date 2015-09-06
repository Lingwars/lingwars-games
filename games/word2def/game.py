#!/usr/bin/env python
# -*- coding: utf-8 -*-

from builtins import input
from apicultur import Apicultur
from random import randint, shuffle

from engine.utils.game import GameBase


import logging
log = logging.getLogger(__name__)

class Game(GameBase):
    def __init__(self, ACCESS_TOKEN_IO, ACCESS_TOKEN_STORE):
        self.api_io = Apicultur(ACCESS_TOKEN_IO, cfg_data='apicultur.io')
        self.api_store = Apicultur(ACCESS_TOKEN_STORE, cfg_data='store.apicultur.com')

    def make_question(self, level, n_options):
        words = self.lookup_words(level, n_options)
        word, options, answer = self.random_question(words, n_options)
        question = {'query': word, 'options': options}
        response = {'answer': answer, 'info': u"%s: %s" % (options[answer][0], options[answer][1])}
        return question, response

    def score(self, response, user_answer):
        print("*"*20)
        print(response)
        print(user_answer)
        r = response.get('answer')
        u = user_answer.get('answer', None)
        try:
            u = int(u)
        except TypeError:
            return 0
        else:
            return 1 if u == response.get('answer') else 0

    def lookup_words(self, level, n):
        log.debug("Game::lookup_words(level=%d, n=%d)" % (level, n))
        words = []
        while (n>len(words)):
            try:
                r = self.api_io.aleatorias_nivel(frecuencia=level)
                for word in r['response']:
                    lema = word['lema']
                    if lema not in [y[0] for y in words]:
                        try:
                            r_def = self.api_store.definicion_10(word=lema)
                            definition = r_def['definicion']
                            words.append((lema, definition))
                            log.debug(" - %s: %s" % (lema, definition))
                        except Exception as e:
                            log.error(" - Exception: %s" % str(e))
            except Exception as e:
                log.error(" - Exception: %s" % str(e))

        return words[:n]

    @classmethod
    def random_question(cls, words, n_options=4, do_shuffle=False):
        log.debug("Game::random_question(words=[], n_options=%d, do_shuffle=%s)" % (n_options, do_shuffle))
        if n_options > len(words):
            raise AttributeError('Not enough options to choose')
        # Randomize?
        if do_shuffle:
            shuffle(words)
        # Choose first word as question an 'n_options' options
        word = words[0][0]
        options = words[:n_options]
        # Shuffle answers and get the index for the correct one
        shuffle(options)
        answer = [y[0] for y in options].index(word)
        # Return
        return word, options, answer


    @classmethod
    def user_level(cls, user_input=True):
        level = randint(0, 9)
        if user_input:
            nivel = input('Indica tu nivel de español de 0 a 9 y pulsa ENTER: ')
            level = int(nivel)
        return level


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    logging.Filter(name='__main__')

    try:
        from secret import ACCESS_TOKEN_IO, ACCESS_TOKEN_STORE
    except ImportError:
        from appweb.secret import ACCESS_TOKEN_IO, ACCESS_TOKEN_STORE

    print("================")
    print("= Definiciones =")
    print("================")

    game = Game(ACCESS_TOKEN_IO, ACCESS_TOKEN_STORE)
    level = game.user_level()
    print(u"Buscando palabras...")
    words = game.lookup_words(level, n=10)
    print(u"Eligiendo pregunta...")
    question = game.random_question(words)

    print(u"¿Cuál es la definición de...")
    print(u">> ...'%s'?" % question['word'])
    options = question['options']
    for i in range(len(options)):
        i += 1
        print(u"\t%d) %s" % (i, options[i-1][1]))

    answer = input(u"\nIntroduce el número respuesta: ")
    answer = int(answer)
    if question['answer'] == answer-1:
        print("\t¡¡BIEN!!")
    else:
        print("\t¡mal!")

