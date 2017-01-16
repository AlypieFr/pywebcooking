# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_mediainrecipe'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='is_comment',
            field=models.BooleanField(default=False),
        ),
    ]
