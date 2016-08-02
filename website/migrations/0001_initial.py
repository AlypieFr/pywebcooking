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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('pseudo', models.CharField(default=None, null=True, max_length=100)),
                ('website', models.CharField(default=None, null=True, max_length=255)),
                ('mail', models.CharField(default=None, null=True, max_length=255)),
                ('content', models.TextField()),
                ('published', models.BooleanField(default=True)),
                ('pub_date', models.DateTimeField(verbose_name='date published', auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='EquipmentInRecipe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('quantity', models.FloatField()),
                ('nb', models.IntegerField()),
                ('equipment', models.ForeignKey(to='website.Equipment')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('level', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='IngredientGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(default='', max_length=255)),
                ('nb', models.IntegerField()),
                ('level', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='IngredientInGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('quantity', models.FloatField()),
                ('unit', models.CharField(max_length=100)),
                ('nb', models.IntegerField()),
                ('ingredient', models.ForeignKey(to='website.Ingredient')),
                ('ingredientGroup', models.ForeignKey(to='website.IngredientGroup')),
            ],
        ),
        migrations.CreateModel(
            name='Instruction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nb', models.IntegerField()),
                ('level', models.IntegerField(default=0)),
                ('text_inst', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nb', models.IntegerField()),
                ('text_cons', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('tps_prep', models.IntegerField()),
                ('tps_rep', models.IntegerField(default=None, null=True)),
                ('tps_cuis', models.IntegerField(default=None, null=True)),
                ('picture_file', models.CharField(max_length=255)),
                ('nb_people', models.IntegerField()),
                ('nb_people_max', models.IntegerField(default=None, null=True)),
                ('pub_date', models.DateTimeField(verbose_name='date published', auto_now=True)),
                ('last_modif', models.DateTimeField(verbose_name='lase modification', auto_now=True)),
                ('excerpt', models.TextField()),
                ('enable_comments', models.BooleanField(default=True)),
                ('published', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField(verbose_name='date published', auto_now=True)),
                ('date_last_connection', models.DateTimeField(verbose_name='date published', auto_now=True)),
                ('group', models.ForeignKey(default=None, to='website.Group', null=True)),
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
            field=models.ManyToManyField(to='website.Equipment', through='website.EquipmentInRecipe'),
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
            field=models.ManyToManyField(to='website.Ingredient', through='website.IngredientInGroup'),
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
        migrations.AlterUniqueTogether(
            name='proposal',
            unique_together=set([('nb', 'recipe')]),
        ),
        migrations.AlterUniqueTogether(
            name='instruction',
            unique_together=set([('nb', 'recipe')]),
        ),
        migrations.AlterUniqueTogether(
            name='ingredientingroup',
            unique_together=set([('ingredientGroup', 'nb')]),
        ),
        migrations.AlterUniqueTogether(
            name='ingredientgroup',
            unique_together=set([('nb', 'recipe')]),
        ),
        migrations.AlterUniqueTogether(
            name='equipmentinrecipe',
            unique_together=set([('nb', 'recipe')]),
        ),
    ]
