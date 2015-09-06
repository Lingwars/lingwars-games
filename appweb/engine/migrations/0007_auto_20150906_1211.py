# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0006_game_is_app'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='is_app',
            field=models.BooleanField(),
        ),
    ]
