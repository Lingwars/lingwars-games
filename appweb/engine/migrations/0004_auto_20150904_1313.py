# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('engine', '0003_game_available'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('first_played', models.DateTimeField(auto_now_add=True)),
                ('last_played', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerScore',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('score', models.PositiveIntegerField(help_text="Work as 'points'. Based on this the engine will compute rankings")),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('player', models.ForeignKey(to='engine.Player')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 9, 4, 11, 13, 55, 987221, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='game',
            field=models.ForeignKey(to='engine.Game'),
        ),
        migrations.AddField(
            model_name='player',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
