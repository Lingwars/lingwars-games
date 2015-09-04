#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.apps import AppConfig, apps
from engine.models import Game, Player

import logging
log = logging.getLogger(__name__)


class GameConfig(AppConfig):
    def register(self):
        self.game, created = Game.objects.get_or_create(name=self.name)
        self.game.title = self.verbose_name
        self.game.available = True
        self.game.save()

    def get_player(self, user):
        if user and user.is_authenticated():
            obj, created = Player.objects.get_or_create(user=user, game__name=self.game.name, defaults={'game': self.game})
            return obj
        return None


def register_games():
    log.info("Available games:")
    Game.objects.all().update(available=False)
    for app in apps.get_app_configs():
        if isinstance(app, GameConfig):
            log.info(u"\t - %s" % app.verbose_name)
            app.register()
