#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<level>\d{1})/play/$', views.question, name='play_level'),
    url(r'^answer/(?P<answer>\d{1})/$', views.answer, name='answer'),
]