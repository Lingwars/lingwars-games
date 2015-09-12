#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

class LevelForm(forms.Form):
    level = forms.ChoiceField([(it, _("Level %d") % it) for it in range(10)])