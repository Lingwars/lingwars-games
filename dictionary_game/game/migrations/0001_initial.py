# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Definition',
            fields=[
                ('word', models.CharField(serialize=False, primary_key=True, max_length=128)),
                ('definition', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('_n_options', models.SmallIntegerField(db_column='n_options')),
                ('_options', models.TextField(db_column='options')),
                ('answer', models.ForeignKey(to='game.Definition', related_name='+')),
                ('query', models.ForeignKey(to='game.Definition')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
