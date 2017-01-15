# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20170115_1549'),
    ]

    operations = [
        migrations.RenameField(
            model_name='proposal',
            old_name='text_cons',
            new_name='text_prop',
        ),
    ]
