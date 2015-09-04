#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.apps import AppConfig, apps
from engine.models import Game

import logging
log = logging.getLogger(__name__)


class GameConfig(AppConfig):
    def register(self):
        obj, created = Game.objects.get_or_create(name=self.name)
        obj.title = self.verbose_name
        obj.available = True
        obj.save()


def register_games():
    log.info("Available games:")
    Game.objects.all().update(available=False)
    for app in apps.get_app_configs():
        if isinstance(app, GameConfig):
            log.info(u"\t - %s" % app.verbose_name)
            app.register()
