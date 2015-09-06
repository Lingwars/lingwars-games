# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0007_auto_20150906_1211'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='name',
            new_name='module',
        ),
    ]
