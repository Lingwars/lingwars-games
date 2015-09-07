#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.views.generic import ListView
from django.apps import apps
from engine.models import Game
from engine.views import GameDetailView, GamePlayView, GameRankingView, UserRankingView


urlpatterns = [
    url(r'^game/list/$', ListView.as_view(queryset=Game.objects.active()), name='game_list'),
    url(r'^user/ranking/$', UserRankingView.as_view(), name='user_ranking'),
    url(r'^game/(?P<pk>\w+)/detail/$', GameDetailView.as_view(), name='game_detail'),
    url(r'^game/(?P<pk>\w+)/play/$', GamePlayView.as_view(), name='game_play'),
    url(r'^game/(?P<pk>\w+)/answer/(?P<uuid>[a-z0-9-]+)/$', GamePlayView.as_view(), name='game_answer'),
    url(r'^game/(?P<pk>\w+)/ranking/$', GameRankingView.as_view(), name='game_ranking'),
]


# This code is executed only once (on first request).
def execute_once():
    engine_app = apps.get_app_config('engine')
    engine_app.register_games()
execute_once()