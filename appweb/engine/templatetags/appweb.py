#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from django import template
from django.core.urlresolvers import reverse, NoReverseMatch

from engine.models import Game

register = template.Library()


@register.simple_tag(takes_context=True)
def active(context, pattern_or_urlname):
    try:
        pattern = '^' + reverse(pattern_or_urlname)
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context['request'].path
    if re.search(pattern, path):
        return 'active'
    return ''


@register.assignment_tag
def get_active_games():
    return Game.objects.active()