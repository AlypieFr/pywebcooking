# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_user_pseudo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='pseudo',
            new_name='url',
        ),
    ]
