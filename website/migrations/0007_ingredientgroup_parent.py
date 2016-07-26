# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_auto_20160726_1920'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredientgroup',
            name='parent',
            field=models.ForeignKey(default=None, to='website.IngredientGroup'),
        ),
    ]
