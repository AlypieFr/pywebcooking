# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_proposal_is_comment'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='mediainrecipe',
            unique_together=set([('media', 'recipe')]),
        ),
    ]
