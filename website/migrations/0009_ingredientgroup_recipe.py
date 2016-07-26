# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_auto_20160726_1931'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredientgroup',
            name='recipe',
            field=models.ForeignKey(to='website.Recipe', default=1),
            preserve_default=False,
        ),
    ]
