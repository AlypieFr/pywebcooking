# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_remove_instruction_level'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredientgroup',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='instruction',
            name='parent',
        ),
        migrations.AddField(
            model_name='ingredientgroup',
            name='level',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='instruction',
            name='level',
            field=models.IntegerField(default=0),
        ),
    ]
