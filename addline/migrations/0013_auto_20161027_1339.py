# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-27 13:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addline', '0012_auto_20161021_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abstractactivity',
            name='operation',
            field=models.CharField(choices=[('Map', 'Map'), ('SplitMap', 'SplitMap'), ('Query', 'Query'), ('Reduce', 'Reduce'), ('Filter', 'Filter')], default='Map', max_length=255),
        ),
        migrations.AlterField(
            model_name='concreteactivity',
            name='operation',
            field=models.CharField(choices=[('Map', 'Map'), ('SplitMap', 'SplitMap'), ('Query', 'Query'), ('Reduce', 'Reduce'), ('Filter', 'Filter')], default='Map', max_length=255),
        ),
        migrations.AlterField(
            model_name='explineactdependency',
            name='optional',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='explineactdependency',
            name='variant',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='explineactivity',
            name='operation',
            field=models.CharField(choices=[('Map', 'Map'), ('SplitMap', 'SplitMap'), ('Query', 'Query'), ('Reduce', 'Reduce'), ('Filter', 'Filter')], default='Map', max_length=255),
        ),
        migrations.AlterField(
            model_name='explineactivity',
            name='optional',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='explineactivity',
            name='variant',
            field=models.BooleanField(default=False),
        ),
    ]