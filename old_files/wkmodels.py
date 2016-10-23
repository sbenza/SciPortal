# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Cactivity(models.Model):
    actid = models.AutoField(unique=True)
    wkfid = models.ForeignKey('Cworkflow', models.DO_NOTHING, db_column='wkfid')
    tag = models.CharField(max_length=50)
    atype = models.CharField(max_length=25)
    description = models.CharField(max_length=250, blank=True, null=True)
    activation = models.TextField(blank=True, null=True)
    constrained = models.CharField(max_length=1, blank=True, null=True)
    templatedir = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cactivity'
        unique_together = (('wkfid', 'actid'),)


class Cextractor(models.Model):
    extid = models.AutoField(unique=True)
    wkfid = models.ForeignKey('Cworkflow', models.DO_NOTHING, db_column='wkfid')
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=25)
    cartridge = models.CharField(max_length=20, blank=True, null=True)
    search = models.CharField(max_length=200, blank=True, null=True)
    invocation = models.TextField(blank=True, null=True)
    delimiter = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cextractor'
        unique_together = (('extid', 'wkfid'),)


class Cfield(models.Model):
    fname = models.CharField(max_length=20)
    relid = models.ForeignKey('Crelation', models.DO_NOTHING, db_column='relid')
    ftype = models.CharField(max_length=10)
    decimalplaces = models.IntegerField(blank=True, null=True)
    fileoperation = models.CharField(max_length=20, blank=True, null=True)
    instrumented = models.CharField(max_length=5, blank=True, null=True)
    extid = models.ForeignKey(Cextractor, models.DO_NOTHING, db_column='extid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cfield'
        unique_together = (('relid', 'fname'),)


class Cjoin(models.Model):
    relid = models.ForeignKey('Crelation', models.DO_NOTHING, db_column='relid')
    innerextid = models.ForeignKey(Cextractor, models.DO_NOTHING, db_column='innerextid')
    outerextid = models.ForeignKey(Cextractor, models.DO_NOTHING, db_column='outerextid')
    fields = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cjoin'
        unique_together = (('relid', 'innerextid', 'outerextid'), ('relid', 'innerextid', 'outerextid'),)


class Cmapping(models.Model):
    cmapid = models.AutoField()
    crelid = models.ForeignKey('Crelation', models.DO_NOTHING, db_column='crelid')
    previousid = models.ForeignKey(Cactivity, models.DO_NOTHING, db_column='previousid', blank=True, null=True)
    nextid = models.ForeignKey(Cactivity, models.DO_NOTHING, db_column='nextid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cmapping'
        unique_together = (('cmapid', 'crelid'),)


class Coperand(models.Model):
    opid = models.AutoField(unique=True)
    actid = models.ForeignKey(Cactivity, models.DO_NOTHING, db_column='actid')
    oname = models.CharField(max_length=100, blank=True, null=True)
    numericvalue = models.FloatField(blank=True, null=True)
    textvalue = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'coperand'
        unique_together = (('actid', 'opid'),)


class Crelation(models.Model):
    wkfid = models.IntegerField()
    relid = models.AutoField(unique=True)
    rtype = models.CharField(max_length=100, blank=True, null=True)
    rname = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crelation'
        unique_together = (('wkfid', 'relid'),)


class Cworkflow(models.Model):
    wkfid = models.AutoField(primary_key=True)
    tag = models.CharField(unique=True, max_length=200)
    description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cworkflow'


class Eactivation(models.Model):
    taskid = models.IntegerField(unique=True)
    actid = models.ForeignKey('Eactivity', models.DO_NOTHING, db_column='actid')
    machineid = models.ForeignKey('Emachine', models.DO_NOTHING, db_column='machineid', blank=True, null=True)
    processor = models.IntegerField(blank=True, null=True)
    exitstatus = models.IntegerField(blank=True, null=True)
    commandline = models.TextField(blank=True, null=True)
    folder = models.CharField(max_length=150, blank=True, null=True)
    subfolder = models.CharField(max_length=50, blank=True, null=True)
    failure_tries = models.IntegerField(blank=True, null=True)
    terr = models.TextField(blank=True, null=True)
    tout = models.TextField(blank=True, null=True)
    starttime = models.DateTimeField(blank=True, null=True)
    endtime = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=25, blank=True, null=True)
    instrumentationstarttime = models.DateTimeField(blank=True, null=True)
    instrumentationendtime = models.DateTimeField(blank=True, null=True)
    computingstarttime = models.DateTimeField(blank=True, null=True)
    computingendtime = models.DateTimeField(blank=True, null=True)
    extractorstarttime = models.DateTimeField(blank=True, null=True)
    extractorendtime = models.DateTimeField(blank=True, null=True)
    dataloadingstarttime = models.DateTimeField(blank=True, null=True)
    dataloadingendtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eactivation'
        unique_together = (('actid', 'taskid'),)


class Eactivity(models.Model):
    actid = models.AutoField(unique=True)
    wkfid = models.ForeignKey('Eworkflow', models.DO_NOTHING, db_column='wkfid')
    tag = models.CharField(max_length=50)
    status = models.CharField(max_length=25, blank=True, null=True)
    starttime = models.DateTimeField(blank=True, null=True)
    endtime = models.DateTimeField(blank=True, null=True)
    cactid = models.ForeignKey(Cactivity, models.DO_NOTHING, db_column='cactid', blank=True, null=True)
    templatedir = models.TextField(blank=True, null=True)
    constrained = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eactivity'
        unique_together = (('wkfid', 'actid'),)


class Ecommperf(models.Model):
    time = models.FloatField(blank=True, null=True)
    sender = models.IntegerField(blank=True, null=True)
    receiver = models.IntegerField(blank=True, null=True)
    ewkfid = models.IntegerField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ecommperf'


class Ecompperf(models.Model):
    time = models.FloatField(blank=True, null=True)
    machineid = models.IntegerField(blank=True, null=True)
    processor = models.IntegerField(blank=True, null=True)
    ewkfid = models.IntegerField(blank=True, null=True)
    taskid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ecompperf'


class Efile(models.Model):
    fileid = models.AutoField(unique=True)
    actid = models.ForeignKey(Eactivity, models.DO_NOTHING, db_column='actid')
    taskid = models.ForeignKey(Eactivation, models.DO_NOTHING, db_column='taskid', blank=True, null=True)
    ftemplate = models.CharField(max_length=1, blank=True, null=True)
    finstrumented = models.CharField(max_length=1, blank=True, null=True)
    fdir = models.CharField(max_length=500, blank=True, null=True)
    fname = models.CharField(max_length=500, blank=True, null=True)
    fsize = models.BigIntegerField(blank=True, null=True)
    fdata = models.DateTimeField(blank=True, null=True)
    foper = models.CharField(max_length=20, blank=True, null=True)
    fieldname = models.CharField(max_length=30, blank=True, null=True)
    indexed = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'efile'
        unique_together = (('actid', 'fileid'),)


class Emachine(models.Model):
    machineid = models.AutoField(primary_key=True)
    hostname = models.CharField(max_length=250)
    address = models.CharField(max_length=250, blank=True, null=True)
    mflopspersecond = models.FloatField(blank=True, null=True)
    type = models.CharField(max_length=250, blank=True, null=True)
    financial_cost = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'emachine'


class Eprovperf(models.Model):
    time = models.FloatField(blank=True, null=True)
    machineid = models.IntegerField(blank=True, null=True)
    ewkfid = models.IntegerField(blank=True, null=True)
    function = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eprovperf'


class Eworkflow(models.Model):
    ewkfid = models.AutoField(primary_key=True)
    tagexec = models.CharField(max_length=200)
    expdir = models.CharField(max_length=150, blank=True, null=True)
    wfdir = models.CharField(max_length=200, blank=True, null=True)
    tag = models.ForeignKey(Cworkflow, models.DO_NOTHING, db_column='tag')
    maximumfailures = models.IntegerField(blank=True, null=True)
    userinteraction = models.CharField(max_length=1, blank=True, null=True)
    reliability = models.FloatField(blank=True, null=True)
    redundancy = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eworkflow'
__author__ = 'sbenza'
