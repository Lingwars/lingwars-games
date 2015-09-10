# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('word2def', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 9, 10, 7, 25, 4, 897802, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
