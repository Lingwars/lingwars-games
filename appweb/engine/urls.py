#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.views.generic import ListView, DetailView
from engine.utils.apps import register_games
from engine.models import Game


urlpatterns = [
    url(r'^game/list/$', ListView.as_view(queryset=Game.objects.active()), name='game_list'),
    url(r'^game/(?P<pk>\d+)/detail/$', DetailView.as_view(queryset=Game.objects.active()), name='game_detail'),
]


# This code is executed only once on first request.
def execute_once():
    register_games()

execute_once()