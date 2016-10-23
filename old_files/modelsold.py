from django.db import models

# Create your models here.
#defining the models for the experiment line, variant activities, abs and concrete wkf
class AbstractWorkflow(models.Model):
    awkfid = models.AutoField(primary_key=True)
    # explineid=models.ForeignKey(ExperimentLine, on_delete=models.CASCADE)

class AbstractActivity(models.Model):
    aactid = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=255)
    operation = models.CharField(max_length=255)

    def __str__(self):
        return str(self.aactid)

class Dependency(models.Model):
    aactid = models.ForeignKey(AbstractActivity, on_delete=models.CASCADE)
    daactid = models.ForeignKey(AbstractActivity, on_delete=models.CASCADE)
    awid = models.ForeignKey(AbstractWorkflow,on_delete=models.CASCADE)


class ConcreteWorkflow(models.Model):
    #tag= models.CharField(max_length=200)
    cwkfid = models.AutoField(primary_key=True)

class ConcreteActivity(models.Model):
    cactid = models.AutoField(primary_key=True)
    cwkfid = models.ForeignKey(ConcreteWorkflow, on_delete=models.CASCADE)
    tag = models.CharField(max_length=255)
    operation = models.CharField(max_length=255)

class ExecutionWorkflow(models.Model):
    #tag= models.CharField(max_length=200)
    ewkfid = models.AutoField(primary_key=True)
    cwkfid = models.ForeignKey(ConcreteWorkflow, on_delete=models.CASCADE)
    starttime = models.IntegerField(blank=True, null=True)
    endtime = models.IntegerField(blank=True, null=True)

class ExecutionActivity(models.Model):
    ewkfid = models.ForeignKey(ExecutionWorkflow, on_delete=models.CASCADE)
    cactid = models.ForeignKey(ConcreteActivity, on_delete=models.CASCADE)
    starttime = models.IntegerField(blank=True, null=True)
    endtime = models.IntegerField(blank=True, null=True)


class ExperimentLine(models.Model):
    explineid = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=255)


#Classes defining the variation of the experiment line
class InvariantActivity(models.Model):
    iactid = models.AutoField(primary_key=True)
    explineid = models.ForeignKey(ExperimentLine, on_delete=models.CASCADE)
    aactid = models.ForeignKey(AbstractActivity, on_delete=models.CASCADE)
    optional = models.BooleanField()

class VariationPoint(models.Model):
    vpointid = models.AutoField(primary_key=True)
    explineid = models.ForeignKey(ExperimentLine,on_delete=models.CASCADE)
    tag = models.CharField(max_length=200)
    optional = models.BooleanField()


class VariantActivity(models.Model):
    vactid = models.AutoField(primary_key=True)
    aactid = models.ForeignKey(AbstractActivity, on_delete=models.CASCADE)
    vpointid = models.ForeignKey(VariationPoint, on_delete=models.CASCADE)

class Derivation(models.Model):
    explineid = models.ForeignKey(ExperimentLine,on_delete=models.CASCADE)
    aactid = models.ForeignKey(AbstractActivity, on_delete=models.CASCADE)
    awkfid = models.ForeignKey(AbstractWorkflow,on_delete=models.CASCADE)

class Instantiation(models.Model):
    cactid = models.ForeignKey(ConcreteActivity,on_delete=models.CASCADE)
    aactid = models.ForeignKey(AbstractActivity, on_delete=models.CASCADE)
    awkfid = models.ForeignKey(AbstractWorkflow,on_delete=models.CASCADE)
    cwkfid = models.ForeignKey(ConcreteWorkflow,on_delete=models.CASCADE)




