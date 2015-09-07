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
        parser.add_argument('--rounds',
                            action='store',
                            dest='rounds',
                            default=1,
                            type=int,
                            help='Number of rounds to play')

    def handle(self, *args, **options):
        id = options.pop('game')
        if id not in self.available_games:
            raise CommandError(u"Invalid game id %r. It must be one of these: %r" % (id, ', '.join(self.available_games)))

        rounds = options.pop('rounds')

        game = engine_app.games[id]
        try:
            game.play_interactive(rounds=rounds, **options)
        except KeyboardInterrupt:
            self.stdout.write(u"User interrupt.")

