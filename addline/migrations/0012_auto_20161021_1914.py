# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-21 19:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addline', '0011_auto_20161021_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abstractactivity',
            name='operation',
            field=models.CharField(choices=[('Map', 'Map'), ('SplitMap', 'SplitMap'), ('Query', 'Query'), ('Reduce', 'Reduce'), ('Filter', 'Filter')], max_length=255),
        ),
        migrations.AlterField(
            model_name='concreteactivity',
            name='operation',
            field=models.CharField(choices=[('Map', 'Map'), ('SplitMap', 'SplitMap'), ('Query', 'Query'), ('Reduce', 'Reduce'), ('Filter', 'Filter')], max_length=255),
        ),
        migrations.AlterField(
            model_name='explineactivity',
            name='operation',
            field=models.CharField(choices=[('Map', 'Map'), ('SplitMap', 'SplitMap'), ('Query', 'Query'), ('Reduce', 'Reduce'), ('Filter', 'Filter')], max_length=255),
        ),
    ]
