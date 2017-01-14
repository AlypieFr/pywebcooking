# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('main', '0004_auto_20170108_1704'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(serialize=False, primary_key=True, to=settings.AUTH_USER_MODEL)),
                ('url', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(verbose_name='auteur', to='main.UserProfile'),
        ),
    ]
