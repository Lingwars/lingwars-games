#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from .views import question, answer


urlpatterns = [
    url(r'^play/$', question, name='play'),
    url(r'^answer/(?P<uuid>[a-z0-9-]+)/(?P<answer>\d{1})/$', answer, name='answer'),
]

