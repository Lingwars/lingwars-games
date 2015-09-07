#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from django.apps import AppConfig, apps

import logging
log = logging.getLogger(__name__)


class GameConfig(AppConfig):
    def get_game(self):
        raise NotImplementedError("GameConfig instances must implement an GameConfig::get_game function")
