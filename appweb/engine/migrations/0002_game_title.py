# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='title',
            field=models.CharField(max_length=128, default=' j '),
            preserve_default=False,
        ),
    ]
