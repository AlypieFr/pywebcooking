# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField(auto_now=True, verbose_name='date published')),
                ('date_last_connection', models.DateTimeField(auto_now=True, verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('tps_prep', models.IntegerField()),
                ('tps_rep', models.IntegerField()),
                ('tps_cuis', models.IntegerField()),
                ('category', models.CharField(max_length=100)),
                ('picture_file', models.CharField(max_length=255)),
                ('nb_poeple', models.IntegerField()),
                ('pub_date', models.DateTimeField(auto_now=True, verbose_name='date published')),
                ('last_modif', models.DateTimeField(auto_now=True, verbose_name='lase modification')),
                ('author', models.ForeignKey(to='website.Author')),
            ],
        ),
    ]
