#!/usr/bin/env python
# -*- coding: utf-8 -*-

class GameBase(object):
    title = None

    @classmethod
    def get_title(cls):
        if not cls.title:
            raise ValueError("Provide a 'title' attribute for your game")
        return cls.title

    def make_question(self, *args, **kwargs):
        raise NotImplementedError()

    def score(self):
        raise NotImplementedError