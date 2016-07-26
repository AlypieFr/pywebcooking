# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_ingredientgroup_nb'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('pseudo', models.CharField(max_length=100, default=None, null=True)),
                ('website', models.CharField(max_length=255, default=None, null=True)),
                ('mail', models.CharField(max_length=255, default=None, null=True)),
                ('content', models.TextField()),
                ('author', models.ForeignKey(to='website.Author', default=None, null=True)),
                ('recipe', models.ForeignKey(to='website.Recipe')),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='EquipmentInRecipe',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('quantity', models.FloatField()),
                ('nb', models.IntegerField()),
                ('equipment', models.ForeignKey(to='website.Equipment')),
                ('recipe', models.ForeignKey(to='website.Recipe')),
            ],
        ),
        migrations.CreateModel(
            name='Instruction',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('nb', models.IntegerField()),
                ('level', models.IntegerField()),
                ('text_inst', models.TextField()),
                ('parent', models.ForeignKey(to='website.Instruction', default=None, null=True)),
                ('recipe', models.ForeignKey(to='website.Recipe')),
            ],
        ),
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('nb', models.IntegerField()),
                ('text_cons', models.TextField()),
                ('recipe', models.ForeignKey(to='website.Recipe')),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='equipment',
            field=models.ManyToManyField(to='website.Equipment', through='website.EquipmentInRecipe'),
        ),
    ]
