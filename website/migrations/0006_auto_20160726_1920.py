# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_auto_20160726_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientgroup',
            name='title',
            field=models.CharField(max_length=255, default=''),
        ),
    ]
