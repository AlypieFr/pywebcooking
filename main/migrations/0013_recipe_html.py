# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20170124_2242'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='html',
            field=models.TextField(null=True, default=None),
        ),
    ]
