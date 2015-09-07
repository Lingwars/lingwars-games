#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.apps import apps

engine_app = apps.get_app_config('engine')


class Command(BaseCommand):
    help = 'Play one round of selected game'

    def __init__(self, *args, **kwargs):
        engine_app.register_games()
        self.available_games = engine_app.games.keys()
        super(Command, self).__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument('game', help=u'One of these: %s' % ', '.join(self.available_games))

    def handle(self, *args, **options):
        id = options['game']
        if id not in self.available_games:
            self.stderr.write(u"Invalid game id %r. It must be one of these: %r" % (id, ', '.join(self.available_games)))

        game = engine_app.games[id]
        game.play_interactive()

