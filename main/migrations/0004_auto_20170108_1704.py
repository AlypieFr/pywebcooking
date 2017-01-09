# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20161231_1705'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipmentinrecipe',
            name='isComment',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='equipmentinrecipe',
            name='quantity',
            field=models.IntegerField(null=True),
        ),
    ]
