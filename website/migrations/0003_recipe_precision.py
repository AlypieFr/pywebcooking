# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20160803_0031'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='precision',
            field=models.CharField(max_length=150, default=None),
        ),
    ]
