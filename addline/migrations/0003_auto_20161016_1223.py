# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-16 12:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('addline', '0002_auto_20161016_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='derivation',
            name='expLine',
            field=models.ForeignKey(db_column='explineid', default=1, on_delete=django.db.models.deletion.CASCADE, to='addline.ExpLine'),
            preserve_default=False,
        ),
    ]