# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('word2def', '0002_question_timestamp'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedWord',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('deleted', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('word', models.ForeignKey(to='word2def.Definition')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='savedword',
            unique_together=set([('word', 'user')]),
        ),
    ]
