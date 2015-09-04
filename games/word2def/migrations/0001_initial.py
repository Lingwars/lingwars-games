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
                ('word', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('definition', models.TextField()),
                ('level', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('level', models.SmallIntegerField()),
                ('_n_options', models.SmallIntegerField(db_column='n_options')),
                ('_options', models.TextField(db_column='options')),
                ('answer', models.ForeignKey(related_name='+', to='word2def.Definition')),
                ('query', models.ForeignKey(to='word2def.Definition')),
                ('user', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
    ]
