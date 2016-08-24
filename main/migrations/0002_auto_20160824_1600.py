# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientingroup',
            name='quantity',
            field=models.FloatField(null=True, default=None),
        ),
        migrations.AlterField(
            model_name='ingredientingroup',
            name='unit',
            field=models.CharField(max_length=100, null=True, default=None),
        ),
    ]
