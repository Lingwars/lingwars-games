#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import time
from builtins import input
from random import randint, shuffle
from collections import deque

from apicultur import Apicultur
from apicultur.utils import ApiculturRateLimitSafe

from engine.utils.game import GameBase, QuestionError


import logging
log = logging.getLogger(__name__)


class Game(GameBase):
    LEVELS = 10
    POOL_SIZE = 10
    question_pool = [deque([]) for _ in range(LEVELS)]  # Structure: [[(q1, r1), (q2, r2)], []]
    thr = threading.Thread()

    def __init__(self, ACCESS_TOKEN_IO, ACCESS_TOKEN_STORE, n_options=4):
        self.api_io = ApiculturRateLimitSafe(ACCESS_TOKEN_IO, cfg_data='apicultur.io')
        self.api_store = ApiculturRateLimitSafe(ACCESS_TOKEN_STORE, cfg_data='store.apicultur.com')

        self.n_options = n_options

    def populate_questions(self):
        log.info("Game.populate_questions()")
        while True:
            for i in range(self.LEVELS):
                log.info(" - level %d" % i)
                if len(self.question_pool[i]) < self.POOL_SIZE:
                    q, r = self._make_question(i, self.n_options)
                    self.question_pool[i].append((q, r))
                    log.info("\t%s" % q['query'])
            time.sleep(1)

    def make_question(self, level, *args, **kwargs):
        assert (level >= 0 and level < Game.LEVELS), "Level out of bounds"
        try:
            return self.question_pool[level].popleft()
        except Exception as e:
            if not self.thr.is_alive():
                self.thr = threading.Thread(target=self.populate_questions, args=(), kwargs={})
                self.thr.start()
            raise QuestionError()

    def _make_question(self, level, n_options, *args, **kwargs):
        word, options, answer = self.random_question(level, n_options)
        return Game.build_question(word, options, answer, level)

    @classmethod
    def build_question(cls, word, options, answer, level):
        question = {'query': word, 'options': [it[1] for it in options], 'level':level}
        response = {'answer': answer, 'options': options, 'info': "%s: %s" % (options[answer][0], options[answer][1])}
        return question, response

    def score(self, response, user_answer):
        r = response.get('answer')
        u = user_answer.get('answer', None)
        try:
            u = int(u)
        except TypeError:
            return 0
        else:
            return 1 if u == response.get('answer') else 0

    def random_question(self, level, n_options):
        words = self.lookup_words(level, n_options)
        word, options, answer = self.get_random_question(words, n_options)
        return word, options, answer

    def lookup_words(self, level, n):
        log.debug("Game::lookup_words(level=%s, n=%s)" % (level, n))
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
    def get_random_question(cls, words, n_options=4, do_shuffle=False):
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

    # Functions to play (user_console)
    def play_config(self):
        level = self.user_level()
        return {'level': level, 'n_options': 3 }

    def play_options(self, question):
        for i in range(len(question['options'])):
            i += 1
        user_input = input("\nIntroduce el número de la respuesta: ")
        user_answer = {'answer': int(user_input)-1}
        return user_answer


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    logging.Filter(name='__main__')

    try:
        from secret import ACCESS_TOKEN_IO, ACCESS_TOKEN_STORE
    except ImportError:
        from appweb.secret import ACCESS_TOKEN_IO, ACCESS_TOKEN_STORE

    game = Game(ACCESS_TOKEN_IO, ACCESS_TOKEN_STORE)
    game.play_interactive(n_options=4)
