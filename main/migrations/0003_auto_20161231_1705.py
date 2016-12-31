# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20160824_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='slug',
            field=models.CharField(verbose_name='slug', unique=True, max_length=255),
        ),
    ]
