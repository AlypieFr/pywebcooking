# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_auto_20160729_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='published',
            field=models.BooleanField(default=True),
        ),
    ]
