# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20160822_0013'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Catégories', 'verbose_name': 'Catégorie'},
        ),
        migrations.AddField(
            model_name='category',
            name='order',
            field=models.IntegerField(verbose_name='order', default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(verbose_name='nom', max_length=100),
        ),
        migrations.AlterField(
            model_name='category',
            name='url',
            field=models.CharField(verbose_name='url', max_length=100),
        ),
    ]
