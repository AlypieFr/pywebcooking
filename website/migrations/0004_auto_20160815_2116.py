# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_recipe_precision'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='precision',
            field=models.CharField(null=True, default=None, max_length=150),
        ),
    ]
