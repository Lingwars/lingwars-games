# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0010_game_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='user',
            field=models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
