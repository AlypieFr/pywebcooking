# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_auto_20160727_1537'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='nb_people_max',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
