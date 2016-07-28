# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_ingredientingroup_unit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instruction',
            name='level',
        ),
    ]
