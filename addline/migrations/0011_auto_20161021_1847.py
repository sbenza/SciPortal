# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-21 18:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('addline', '0010_auto_20161021_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abstractactivity',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='abstractactivity',
            name='operation',
            field=models.CharField(choices=[(1, 'Map'), (2, 'SplitMap'), (3, 'Query'), (4, 'Reduce'), (5, 'Filter')], max_length=255),
        ),
        migrations.AlterField(
            model_name='abstractworkflow',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='abstractworkflowdependency',
            name='activity',
            field=models.ForeignKey(db_column='derivationid', on_delete=django.db.models.deletion.CASCADE, related_name='derivationid', to='addline.Derivation'),
        ),
        migrations.AlterField(
            model_name='abstractworkflowdependency',
            name='dependentActivity',
            field=models.ForeignKey(db_column='depderivationid', on_delete=django.db.models.deletion.CASCADE, related_name='depderivationid', to='addline.Derivation'),
        ),
        migrations.AlterField(
            model_name='concreteactivity',
            name='concreteWorkflow',
            field=models.ForeignKey(db_column='concreteworkflowid', on_delete=django.db.models.deletion.CASCADE, to='addline.Concreteworkflow'),
        ),
        migrations.AlterField(
            model_name='concreteactivity',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='concreteactivity',
            name='operation',
            field=models.CharField(choices=[(1, 'Map'), (2, 'SplitMap'), (3, 'Query'), (4, 'Reduce'), (5, 'Filter')], max_length=255),
        ),
        migrations.AlterField(
            model_name='derivation',
            name='abstractActivity',
            field=models.ForeignKey(db_column='abstractactivityid', on_delete=django.db.models.deletion.CASCADE, to='addline.AbstractActivity'),
        ),
        migrations.AlterField(
            model_name='derivation',
            name='abstractWorkflow',
            field=models.ForeignKey(db_column='abstractworkflowid', on_delete=django.db.models.deletion.CASCADE, to='addline.AbstractWorkflow'),
        ),
        migrations.AlterField(
            model_name='derivation',
            name='expLineActivity',
            field=models.ForeignKey(db_column='explineactid', on_delete=django.db.models.deletion.CASCADE, to='addline.ExpLineActivity'),
        ),
        migrations.AlterField(
            model_name='expline',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='explineactdependency',
            name='dependentELActivity',
            field=models.ForeignKey(db_column='depexplineactid', on_delete=django.db.models.deletion.CASCADE, related_name='dependentELActivity', to='addline.ExpLineActivity'),
        ),
        migrations.AlterField(
            model_name='explineactdependency',
            name='eLActivity',
            field=models.ForeignKey(db_column='explineactid', on_delete=django.db.models.deletion.CASCADE, related_name='eLActivity', to='addline.ExpLineActivity'),
        ),
        migrations.AlterField(
            model_name='explineactivity',
            name='expLine',
            field=models.ForeignKey(db_column='explineid', on_delete=django.db.models.deletion.CASCADE, to='addline.ExpLine'),
        ),
        migrations.AlterField(
            model_name='explineactivity',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='explineactivity',
            name='operation',
            field=models.CharField(choices=[(1, 'Map'), (2, 'SplitMap'), (3, 'Query'), (4, 'Reduce'), (5, 'Filter')], max_length=255),
        ),
        migrations.AlterField(
            model_name='instantiation',
            name='abstractActivity',
            field=models.ForeignKey(db_column='abstractactivityid', on_delete=django.db.models.deletion.CASCADE, to='addline.AbstractActivity'),
        ),
        migrations.AlterField(
            model_name='instantiation',
            name='abstractWorkflow',
            field=models.ForeignKey(db_column='abstractworkflowid', on_delete=django.db.models.deletion.CASCADE, to='addline.AbstractWorkflow'),
        ),
        migrations.AlterField(
            model_name='instantiation',
            name='concreteActivity',
            field=models.ForeignKey(db_column='concreteactivityid', on_delete=django.db.models.deletion.CASCADE, to='addline.Concreteactivity'),
        ),
        migrations.AlterField(
            model_name='instantiation',
            name='concreteWorkflow',
            field=models.ForeignKey(db_column='concreteworkflowid', on_delete=django.db.models.deletion.CASCADE, to='addline.Concreteworkflow'),
        ),
    ]