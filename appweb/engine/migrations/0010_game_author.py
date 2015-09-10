# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0009_auto_20150907_1059'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='author',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]
