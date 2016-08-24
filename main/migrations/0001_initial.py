# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='nom', max_length=100)),
                ('url', models.CharField(verbose_name='url', max_length=100)),
                ('order', models.IntegerField(verbose_name='ordre', unique=True)),
            ],
            options={
                'verbose_name': 'Catégorie',
                'verbose_name_plural': 'Catégories',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('pseudo', models.CharField(default=None, max_length=100, null=True)),
                ('website', models.CharField(default=None, max_length=255, null=True)),
                ('mail', models.CharField(default=None, max_length=255, null=True)),
                ('content', models.TextField()),
                ('published', models.BooleanField(default=True)),
                ('pub_date', models.DateTimeField(verbose_name='date published', auto_now=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='EquipmentInRecipe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('quantity', models.IntegerField()),
                ('nb', models.IntegerField()),
                ('equipment', models.ForeignKey(to='main.Equipment')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('level', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='IngredientGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=255, default='')),
                ('nb', models.IntegerField()),
                ('level', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='IngredientInGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('quantity', models.FloatField()),
                ('unit', models.CharField(max_length=100)),
                ('nb', models.IntegerField()),
                ('ingredient', models.ForeignKey(to='main.Ingredient')),
                ('ingredientGroup', models.ForeignKey(to='main.IngredientGroup')),
            ],
        ),
        migrations.CreateModel(
            name='Instruction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('nb', models.IntegerField()),
                ('level', models.IntegerField(default=0)),
                ('text_inst', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('nb', models.IntegerField()),
                ('text_cons', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(verbose_name='titre', max_length=255)),
                ('description', models.TextField(verbose_name='description')),
                ('tps_prep', models.IntegerField(verbose_name='temps de préparation')),
                ('tps_rep', models.IntegerField(verbose_name='temps de repos', default=None, null=True)),
                ('tps_cuis', models.IntegerField(verbose_name='temps de cuisson', default=None, null=True)),
                ('picture_file', models.CharField(verbose_name="fichier d'illustration", max_length=255)),
                ('nb_people', models.IntegerField(verbose_name='nombre de personnes')),
                ('nb_people_max', models.IntegerField(verbose_name='nombre de personnes max', default=None, null=True)),
                ('precision', models.CharField(verbose_name='précision', default=None, max_length=150, null=True)),
                ('pub_date', models.DateTimeField(verbose_name='date de publication', auto_now=True)),
                ('last_modif', models.DateTimeField(verbose_name='dernière modification', auto_now=True)),
                ('excerpt', models.TextField(verbose_name='résumé')),
                ('enable_comments', models.BooleanField(verbose_name='activer les commentaires', default=True)),
                ('published', models.BooleanField(verbose_name='publié', default=True)),
                ('slug', models.CharField(verbose_name='slug', max_length=255)),
                ('author', models.ForeignKey(verbose_name='auteur', to=settings.AUTH_USER_MODEL)),
                ('category', models.ManyToManyField(verbose_name='catégorie', to='main.Category')),
                ('equipment', models.ManyToManyField(verbose_name='Matériel nécessaire', through='main.EquipmentInRecipe', to='main.Equipment')),
            ],
            options={
                'verbose_name': 'Recette',
                'verbose_name_plural': 'Recettes',
            },
        ),
        migrations.AddField(
            model_name='proposal',
            name='recipe',
            field=models.ForeignKey(to='main.Recipe'),
        ),
        migrations.AddField(
            model_name='instruction',
            name='recipe',
            field=models.ForeignKey(to='main.Recipe'),
        ),
        migrations.AddField(
            model_name='ingredientgroup',
            name='ingredients',
            field=models.ManyToManyField(through='main.IngredientInGroup', to='main.Ingredient'),
        ),
        migrations.AddField(
            model_name='ingredientgroup',
            name='recipe',
            field=models.ForeignKey(to='main.Recipe'),
        ),
        migrations.AddField(
            model_name='equipmentinrecipe',
            name='recipe',
            field=models.ForeignKey(to='main.Recipe'),
        ),
        migrations.AddField(
            model_name='comment',
            name='recipe',
            field=models.ForeignKey(to='main.Recipe'),
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
