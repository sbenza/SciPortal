# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-19 15:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('addline', '0003_auto_20161016_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='abstractworkflowdependency',
            name='expLine',
            field=models.ForeignKey(db_column='explineid', default=1, on_delete=django.db.models.deletion.CASCADE, to='addline.ExpLine'),
            preserve_default=False,
        ),
    ]