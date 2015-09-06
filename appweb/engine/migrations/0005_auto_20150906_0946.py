# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0004_auto_20150904_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerscore',
            name='score',
            field=models.FloatField(help_text="Work as 'points'. Based on this the engine will compute rankings"),
        ),
    ]
