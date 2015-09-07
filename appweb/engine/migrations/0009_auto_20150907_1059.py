# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0008_auto_20150906_1920'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='module',
        ),
        migrations.AlterField(
            model_name='game',
            name='id',
            field=models.CharField(max_length=40, primary_key=True, serialize=False),
        ),
    ]
