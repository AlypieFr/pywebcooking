# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20170115_1350'),
    ]

    operations = [
        migrations.RenameField(
            model_name='equipmentinrecipe',
            old_name='isComment',
            new_name='is_comment',
        ),
    ]
