# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-28 19:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('addline', '0014_auto_20161027_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='abstractworkflow',
            name='expLineActivity',
            field=models.ForeignKey(db_column='explineactid', default=1, on_delete=django.db.models.deletion.CASCADE, to='addline.ExpLineActivity'),
            preserve_default=False,
        ),
    ]