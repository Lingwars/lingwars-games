# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='definition',
            name='level',
            field=models.SmallIntegerField(default=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='level',
            field=models.SmallIntegerField(default=10),
            preserve_default=False,
        ),
    ]
