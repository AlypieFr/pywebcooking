# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='nb_poeple',
            new_name='nb_people',
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tps_cuis',
            field=models.IntegerField(null=True, default=None),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tps_rep',
            field=models.IntegerField(null=True, default=None),
        ),
    ]
