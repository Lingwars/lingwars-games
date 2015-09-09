#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from django.conf.urls import include, url
from django.views.generic import ListView, TemplateView
from django.apps import apps
from .models import Game
from .views import GameDetailView, GamePlayView, GameRankingView, UserRankingView


urlpatterns = [
    url(r'^home/$', TemplateView.as_view(template_name='engine/home.html'), name='games'),

    url(r'^(?P<pk>\w+)/detail/$', GameDetailView.as_view(), name='game_detail'),
    url(r'^(?P<pk>\w+)/play/$', GamePlayView.as_view(), name='game_play'),
    url(r'^(?P<pk>\w+)/answer/(?P<uuid>[a-z0-9-]+)/$', GamePlayView.as_view(), name='game_answer'),
    url(r'^(?P<pk>\w+)/ranking/$', GameRankingView.as_view(), name='game_ranking'),

    url(r'^user/ranking/$', UserRankingView.as_view(), name='user_ranking'),
]


# This code is executed only once (on first request).
def execute_once():
    engine_app = apps.get_app_config('engine')
    engine_app.register_games()
execute_once()