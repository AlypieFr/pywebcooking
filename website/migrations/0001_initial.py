# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('pseudo', models.CharField(max_length=100, null=True, default=None)),
                ('website', models.CharField(max_length=255, null=True, default=None)),
                ('mail', models.CharField(max_length=255, null=True, default=None)),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='EquipmentInRecipe',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('quantity', models.FloatField()),
                ('nb', models.IntegerField()),
                ('equipment', models.ForeignKey(to='website.Equipment')),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='IngredientGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=255, default='')),
                ('nb', models.IntegerField()),
                ('level', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='IngredientInGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('quantity', models.FloatField()),
                ('unit', models.CharField(max_length=100)),
                ('ingredient', models.ForeignKey(to='website.Ingredient')),
                ('ingredientGroup', models.ForeignKey(to='website.IngredientGroup')),
            ],
        ),
        migrations.CreateModel(
            name='Instruction',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('nb', models.IntegerField()),
                ('level', models.IntegerField()),
                ('text_inst', models.TextField()),
                ('parent', models.ForeignKey(default=None, to='website.Instruction', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('nb', models.IntegerField()),
                ('text_cons', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('tps_prep', models.IntegerField()),
                ('tps_rep', models.IntegerField()),
                ('tps_cuis', models.IntegerField()),
                ('picture_file', models.CharField(max_length=255)),
                ('nb_poeple', models.IntegerField()),
                ('pub_date', models.DateTimeField(verbose_name='date published', auto_now=True)),
                ('last_modif', models.DateTimeField(verbose_name='lase modification', auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField(verbose_name='date published', auto_now=True)),
                ('date_last_connection', models.DateTimeField(verbose_name='date published', auto_now=True)),
                ('role', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(to='website.User'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='category',
            field=models.ManyToManyField(to='website.Category'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='equipment',
            field=models.ManyToManyField(through='website.EquipmentInRecipe', to='website.Equipment'),
        ),
        migrations.AddField(
            model_name='proposal',
            name='recipe',
            field=models.ForeignKey(to='website.Recipe'),
        ),
        migrations.AddField(
            model_name='instruction',
            name='recipe',
            field=models.ForeignKey(to='website.Recipe'),
        ),
        migrations.AddField(
            model_name='ingredientgroup',
            name='ingredients',
            field=models.ManyToManyField(through='website.IngredientInGroup', to='website.Ingredient'),
        ),
        migrations.AddField(
            model_name='ingredientgroup',
            name='parent',
            field=models.ForeignKey(default=None, to='website.IngredientGroup', null=True),
        ),
        migrations.AddField(
            model_name='ingredientgroup',
            name='recipe',
            field=models.ForeignKey(to='website.Recipe'),
        ),
        migrations.AddField(
            model_name='equipmentinrecipe',
            name='recipe',
            field=models.ForeignKey(to='website.Recipe'),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(default=None, to='website.User', null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='recipe',
            field=models.ForeignKey(to='website.Recipe'),
        ),
    ]
