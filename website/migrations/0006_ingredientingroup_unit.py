# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_recipe_nb_people_max'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredientingroup',
            name='unit',
            field=models.CharField(max_length=100, default=''),
            preserve_default=False,
        ),
    ]
