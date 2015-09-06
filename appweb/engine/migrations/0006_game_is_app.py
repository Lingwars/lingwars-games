# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0005_auto_20150906_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='is_app',
            field=models.BooleanField(default=False),
        ),
    ]
