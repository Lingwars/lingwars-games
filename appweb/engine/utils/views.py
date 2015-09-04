#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.apps import apps
from engine.models import PlayerScore


class GameHelper(object):
    app_label = None

    def __init__(self, app_label=None, *args, **kwargs):
        super(GameHelper, self).__init__(*args, **kwargs)
        self.app_label = app_label or self.app_label
        self.app = apps.get_app_config(self.app_label)

    def get_player(self, user):
        if not hasattr(self, '_player'):
            player = self.app.get_player(user)
            player.touch()  # TODO: Where to touch and update 'last_seen'??
            setattr(self, '_player', player)
        return getattr(self, '_player')

    def score(self, user, score):
        player = self.get_player(user)
        PlayerScore.objects.create(player=player, score=score)
        player.touch()