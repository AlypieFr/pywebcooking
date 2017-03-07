# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_recipe_html'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='last_modif',
            field=models.DateTimeField(verbose_name='dernière modification'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='pub_date',
            field=models.DateTimeField(verbose_name='date de publication'),
        ),
    ]
