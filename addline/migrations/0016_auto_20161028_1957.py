# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-28 19:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('addline', '0015_abstractworkflow_explineactivity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='abstractworkflow',
            name='expLineActivity',
        ),
        migrations.AddField(
            model_name='abstractworkflow',
            name='expLine',
            field=models.ForeignKey(db_column='explineid', default=1, on_delete=django.db.models.deletion.CASCADE, to='addline.ExpLine'),
            preserve_default=False,
        ),
    ]