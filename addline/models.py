from django.db import models



OPERATION_CHOICES = ( ('Map', 'Map'),
                      ('SplitMap', 'SplitMap'),
                      ('Query', 'Query'),
                      ('Reduce', 'Reduce'),
                      ('Filter', 'Filter'),
)
# Create your models here.
# defining the models for the experiment line, variant activities, abs and concrete wkf
class AbstractActivity(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    operation = models.CharField(max_length=255,  choices=OPERATION_CHOICES)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'abstractactivity'


class AbstractWorkflow(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'abstractworkflow'





class Concreteactivity(models.Model):
    id = models.AutoField(primary_key=True)
    concreteWorkflow = models.ForeignKey('ConcreteWorkflow', on_delete=models.CASCADE, db_column='concreteworkflowid',
                                         )
    name = models.CharField(max_length=255)
    operation = models.CharField(max_length=255, choices=OPERATION_CHOICES, default='Map')

    class Meta:
        db_table = 'concreteactivity'


class Concreteworkflow(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        db_table = 'concreteworkflow'


class Derivation(models.Model):
    id = models.AutoField(primary_key=True)
    expLineActivity = models.ForeignKey('ExpLineActivity', on_delete=models.CASCADE, db_column='explineactid')
    abstractWorkflow = models.ForeignKey('AbstractWorkflow', on_delete=models.CASCADE, db_column='abstractworkflowid')
    abstractActivity = models.ForeignKey('AbstractActivity', on_delete=models.CASCADE, db_column='abstractactivityid')

    class Meta:
        db_table = 'derivation'


class ExpLine(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'expline'


class ExpLineActivity(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    operation = models.CharField(max_length=255, choices=OPERATION_CHOICES)
    variant = models.BooleanField(default=False)
    optional = models.BooleanField(default=False)
    expLine = models.ForeignKey('ExpLine', on_delete=models.CASCADE, db_column='explineid')

    class Meta:
        db_table = 'explineactivity'


class AbstractWorkflowDependency(models.Model):
    id = models.AutoField(primary_key=True)
    activity = models.ForeignKey('Derivation', on_delete=models.CASCADE, db_column='derivationid', related_name='derivationid')
    dependentActivity = models.ForeignKey('Derivation', on_delete=models.CASCADE, db_column='depderivationid', related_name='depderivationid')
    class Meta:
        db_table = 'abstractworkflowdependency'


class ExpLineActDependency(models.Model):
    id = models.AutoField(primary_key=True)
    eLActivity = models.ForeignKey(ExpLineActivity, on_delete=models.CASCADE, db_column='explineactid', related_name='eLActivity')
    dependentELActivity = models.ForeignKey(ExpLineActivity, on_delete=models.CASCADE, db_column='depexplineactid',
                                            related_name='dependentELActivity')
    variant = models.BooleanField(default=False)
    optional = models.BooleanField(default=False)


    class Meta:
        db_table = 'explineactdependency'


class Instantiation(models.Model):
    abstractWorkflow = models.ForeignKey('AbstractWorkflow', on_delete=models.CASCADE, db_column='abstractworkflowid',
                                         )
    concreteWorkflow = models.ForeignKey('ConcreteWorkflow', on_delete=models.CASCADE, db_column='concreteworkflowid',
                                         )
    abstractActivity = models.ForeignKey('AbstractActivity', on_delete=models.CASCADE, db_column='abstractactivityid',
                                        )
    concreteActivity = models.ForeignKey('ConcreteActivity', on_delete=models.CASCADE, db_column='concreteactivityid',
                                         )

    class Meta:
        db_table = 'instantiation'
