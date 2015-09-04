#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^play/$', TemplateView.as_view(template_name='word2def/game_play.html'), name='play'),
]

