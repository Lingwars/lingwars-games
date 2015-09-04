# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0002_game_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='available',
            field=models.BooleanField(default=True),
        ),
    ]
