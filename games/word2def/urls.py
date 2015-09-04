#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from .views import QuestionView


urlpatterns = [
    url(r'^play/$', QuestionView.as_view(), name='play'),
    url(r'^answer/(?P<uuid>[a-z0-9-]+)/$', QuestionView.as_view(), name='answer'),
]

