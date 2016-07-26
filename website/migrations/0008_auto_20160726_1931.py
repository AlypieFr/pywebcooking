# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_ingredientgroup_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientgroup',
            name='parent',
            field=models.ForeignKey(to='website.IngredientGroup', null=True, default=None),
        ),
    ]
