# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Abstractactivity(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    operation = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'abstractactivity'


class Abstractworkflow(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'abstractworkflow'


class Abstractworkflowdependency(models.Model):
    id = models.IntegerField(primary_key=True)
    derivationid = models.ForeignKey('Derivation', models.DO_NOTHING, db_column='derivationid', blank=True, null=True)
    depderivationid = models.ForeignKey('Derivation', models.DO_NOTHING, db_column='depderivationid', blank=True, null=True)

    class Meta:
        db_table = 'abstractworkflowdependency'


class Concreteactivity(models.Model):
    id = models.IntegerField(primary_key=True)
    concreteworkflowid = models.ForeignKey('Concreteworkflow', models.DO_NOTHING, db_column='concreteworkflowid', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    operation = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'concreteactivity'


class Concreteworkflow(models.Model):
    id = models.IntegerField(primary_key=True)

    class Meta:
        db_table = 'concreteworkflow'


class Derivation(models.Model):
    id = models.IntegerField(primary_key=True)
    explineactid = models.ForeignKey('Explineactivity', models.DO_NOTHING, db_column='explineactid', blank=True, null=True)
    abstractworkflowid = models.ForeignKey('Abstractworkflow', models.DO_NOTHING, db_column='abstractworkflowid', blank=True, null=True)
    abstractactivityid = models.ForeignKey('Abstractactivity', models.DO_NOTHING, db_column='abstractactivityid', blank=True, null=True)

    class Meta:
        db_table = 'derivation'


class Expline(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'expline'


class Explineactdependency(models.Model):
    id = models.IntegerField(primary_key=True)
    explineactid = models.ForeignKey('Explineactivity', models.DO_NOTHING, db_column='explineactid', blank=True, null=True)
    depexplineactid = models.ForeignKey('Explineactivity', models.DO_NOTHING, db_column='depexplineactid', blank=True, null=True)
    variant = models.NullBooleanField()
    optional = models.NullBooleanField()

    class Meta:
        db_table = 'explineactdependency'


class Explineactivity(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    operation = models.CharField(max_length=255, blank=True, null=True)
    variant = models.NullBooleanField()
    optional = models.NullBooleanField()
    explineid = models.ForeignKey('Expline', models.DO_NOTHING, db_column='explineid', blank=True, null=True)

    class Meta:
        db_table = 'explineactivity'


class Instantiation(models.Model):
    abstractworkflowid = models.ForeignKey('Abstractworkflow', models.DO_NOTHING, db_column='abstractworkflowid', blank=True, null=True)
    concreteworkflowid = models.ForeignKey('Concreteworkflow', models.DO_NOTHING, db_column='concreteworkflowid', blank=True, null=True)
    abstractactivityid = models.ForeignKey('Abstractactivity', models.DO_NOTHING, db_column='abstractactivityid', blank=True, null=True)
    concreteactivityid = models.ForeignKey('Concreteactivity', models.DO_NOTHING, db_column='concreteactivityid', blank=True, null=True)

    class Meta:
        db_table = 'instantiation'
