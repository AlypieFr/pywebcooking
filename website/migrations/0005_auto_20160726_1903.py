# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_remove_ingredient_type_ingr'),
    ]

    operations = [
        migrations.CreateModel(
            name='IngredientGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('level', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='IngredientInGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('quantity', models.FloatField()),
                ('unit', models.CharField(max_length=100)),
                ('ingredient', models.ForeignKey(to='website.Ingredient')),
                ('ingredientGroup', models.ForeignKey(to='website.IngredientGroup')),
            ],
        ),
        migrations.AddField(
            model_name='ingredientgroup',
            name='ingredients',
            field=models.ManyToManyField(to='website.Ingredient', through='website.IngredientInGroup'),
        ),
    ]
