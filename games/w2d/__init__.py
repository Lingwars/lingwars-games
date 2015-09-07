#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from .game import Game

try:
    from django.conf import settings
    ACCESS_TOKEN_IO = getattr(settings, 'ACCESS_TOKEN_IO')
    ACCESS_TOKEN_STORE = getattr(settings, 'ACCESS_TOKEN_STORE')
except ImportError:
    from secret import ACCESS_TOKEN_IO, ACCESS_TOKEN_STORE

game = Game(ACCESS_TOKEN_IO, ACCESS_TOKEN_STORE)