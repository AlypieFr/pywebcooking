# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20170115_1628'),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaInRecipe',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('media', models.CharField(unique=True, max_length=255)),
                ('type', models.CharField(choices=[('main', 'main_picture'), ('other', 'other_picutre')], max_length=5)),
                ('recipe', models.ForeignKey(to='main.Recipe')),
            ],
        ),
    ]
