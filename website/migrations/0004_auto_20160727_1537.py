# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_auto_20160727_1532'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredientgroup',
            name='level',
        ),
        migrations.RemoveField(
            model_name='ingredientingroup',
            name='unit',
        ),
        migrations.AddField(
            model_name='ingredientingroup',
            name='nb',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
