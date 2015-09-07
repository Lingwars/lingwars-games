#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
from django.apps import AppConfig, apps
from django.conf import settings
from django.utils.module_loading import import_string
from .models import Game
from .utils.apps import GameConfig

import logging
log = logging.getLogger(__name__)


def assert_game(instance):
    # TODO: Implement game type traits
    pass

class EngineAppConfig(AppConfig):
    name = 'engine'
    games = {}

    def register_games(self):
        log.info("Available games:")
        Game.objects.all().update(available=False, is_app=False)

        # Registered apps
        app_games_module = []
        for app in apps.get_app_configs():
            if isinstance(app, GameConfig):
                app_games_module.append(app.module.__path__[0])
                log.info(u"\t - %s: %s" % (app.name, app.verbose_name))
                id = app.name.rsplit('.', 1)[1]
                if Game.objects.filter(id=id, available=True).exists():
                    raise RuntimeError(u"A game with id '%s' already exists" % id)

                game = app.get_game()
                assert_game(game)

                obj, created = Game.objects.get_or_create(id=str(id), defaults={'title': app.verbose_name, 'is_app': True})
                obj.available = True
                obj.is_app = True
                obj.save()
                self.games[id] = game

        # TODO: Not registered apps (found by directory)
        #   -- do I want to consider these? No, all game-apps must be in INSTALLED_APPS or they will be considered as non-app-games

        # Simple games, just a 'game.py' file inside dir
        for dir in getattr(settings, 'LINGWARS_GAMES_DIRS', []):
            for item in os.listdir(dir):
                current_path = os.path.abspath(os.path.join(dir, item))
                if current_path in app_games_module:
                    #log.debug(u"\t%s already included as app-game" % current_path)
                    pass
                else:
                    try:
                        module = '%s.game' % (item)
                        game = import_string(module)
                        assert_game(game)
                        log.info(u"\t - %s" % module)

                        obj, created = Game.objects.get_or_create(id=str(item), defaults={'title': getattr(game, 'title', item), 'is_app': False})
                        obj.available = True
                        obj.is_app = False
                        obj.save()
                        self.games[item] = game
                    except ImportError as e:
                        log.warn(u"\t - %s: does not contain a game object" % module)





