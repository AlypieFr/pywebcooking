# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_auto_20160729_0014'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='enable_comments',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='excerpt',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recipe',
            name='published',
            field=models.BooleanField(default=True),
        ),
    ]
