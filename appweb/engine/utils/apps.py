#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import sys
from django.apps import AppConfig, apps
from django.conf import settings
from django.utils.module_loading import import_string

from ..models import Game, Player, PlayerScore
from .game import GameBase


import logging
log = logging.getLogger(__name__)


def is_game(game_module):
    GameClass = import_string(game_module)
    if not issubclass(GameClass, GameBase):
        raise AttributeError(u"It seems that you are creating a game at %r but Game class does not inherit form 'engine.utils.game.GameBase'" % game_module)
    return True


class GameConfig(AppConfig):
    def get_module(self):
        return '%s.game.Game' % self.name

    def register(self):
        if is_game(self.get_module()):
            self.game, created = Game.objects.get_or_create(name=self.get_module(), defaults={'is_app': True})
            self.game.title = self.verbose_name
            self.game.available = True
            self.game.is_app = True
            self.game.save()

    def get_player(self, user):
        if user and user.is_authenticated():
            obj, created = Player.objects.get_or_create(user=user, game__name=self.game.name, defaults={'game': self.game})
            return obj
        return None

    def score(self, user, score):
        player = self.get_player(user)
        if player:
            PlayerScore.objects.create(player=player, score=score)
            player.touch()


def register_games():
    log.info("Available games:")
    Game.objects.all().update(available=False, is_app=False)
    # Registered apps
    for app in apps.get_app_configs():
        if isinstance(app, GameConfig):
            log.info(u"\t - %s" % app.verbose_name)
            app.register()
    # TODO: Not registered apps (found by directory)

    # TODO: Simple games, just a 'game.py' file inside dir
    # dir = settings.get('GAME_DIRS', [])
    base_dir = getattr(settings, 'BASE_DIR', '')
    dir = os.path.join(base_dir, '../games')
    # Add to path
    import sys
    sys.path.append(dir)
    print(u"Look for games at %r" % dir)
    for item in os.listdir(dir):
        game_file = os.path.join(dir, item, 'game.py')
        # TODO: discriminate bw app-game and single-game
        if os.path.isfile(game_file) and not os.path.isfile(os.path.join(dir, item, 'models.py')):
            print(u" -- %s: %s" % (item, game_file))
            game_module = '%s.game.Game' % item
            if is_game(game_module):
                GameClass = import_string(game_module)
                game, created = Game.objects.get_or_create(name=game_module, defaults={'is_app': False})
                game.title = GameClass.get_title()
                game.available = True
                game.is_app = False
                game.save()




