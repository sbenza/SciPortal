from pyDatalog import pyDatalog

#
# class AbstractActivityDataLog(pyDatalog.Mixin):
#     def __init__(self, abstractActivity):
#         # call the initialization method of the Mixin class
#         super(AbstractActivityDataLog, self).__init__()
#         id = abstractActivity.id
#         name = abstractActivity.name
#         operation = abstractActivity.operation
#         description = abstractActivity.description
#
#     def __repr__(self):  # specifies how to display an AbstractActivityDataLog
#         return self.name
#
#
# class AbstractWorkflowDataLog(pyDatalog.Mixin):
#     def __init__(self, abstractWorkflow):
#         super(AbstractWorkflowDataLog, self).__init__()
#
#         id = abstractWorkflow.id
#         name = abstractWorkflow.name
#         description = abstractWorkflow.description
#         expLine = abstractWorkflow.expLine
#
#     def __repr__(self):  # specifies how to display an AbstractWorkflowDataLog
#         return self.name
#
#
# class ConcreteActivityDataLog(pyDatalog.Mixin):
#     def __init__(self, concreteActivity):
#         super(ConcreteActivityDataLog, self).__init__()
#
#         id = concreteActivity.id
#         concreteWorkflow = concreteActivity.concreteWorkflow
#         name = concreteActivity.name
#         operation = concreteActivity.operation
#
#     def __repr__(self):  # specifies how to display an ConcreteActivityDataLog
#         return self.name
#
#
# class ConcreteWorkflowDataLog(pyDatalog.Mixin):
#     def __init__(self, concreteWorkflow):
#         super(ConcreteWorkflowDataLog, self).__init__()
#
#         id = concreteWorkflow.id
#
#     def __repr__(self):  # specifies how to display an ConcreteWorkflowDataLog
#         return self.id
#
#
# class DerivationDataLog(pyDatalog.Mixin):
#     def __init__(self, derivation):
#         super(DerivationDataLog, self).__init__()
#
#         id = derivation.id
#         expLineActivity = derivation.expLineActivity
#         abstractWorkflow = derivation.abstractWorkflow
#         abstractActivity = derivation.abstractActivity
#
#     def __repr__(self):  # specifies how to display an DerivationDataLog
#         return self.id


class ExpLineDataLog(pyDatalog.Mixin):
    def __init__(self, expLine):
        # call the initialization method of the Mixin class
        super(ExpLineDataLog, self).__init__()
        self.id = expLine.id
        self.name = expLine.name
        self.description = expLine.description

    def __repr__(self):  # specifies how to display an ExpLineDataLog
        return self.name


class ExpLineActivityDataLog(pyDatalog.Mixin):
    def __init__(self, ela):
        # call the initialization method of the Mixin class
        super(ExpLineActivityDataLog, self).__init__()
        self.id = ela.id
        self.name = ela.name
        self.operation = ela.operation
        self.variant = ela.variant
        self.optional = ela.optional
        self.expLine = ExpLineDataLog(ela.expLine)
    def __repr__(self):  # specifies how to display an ExpLineActivityDataLog
        return self.name

    # pyDatalog.clear()
    # @pyDatalog.program()
    # def _(self):

        # ExpLineActivityDataLog.activity_of(X, Y) <= (ExpLineActivityDataLog.expLine[X]==Y)
        # ExpLineActivityDataLog.activity_list(X,Y) <= (ExpLineActivityDataLog.expLine[X]==Z) & (Z != None) & (X!=Y)

# class AbstractWorkflowDependencyDataLog(pyDatalog.Mixin):
#     def __init__(self, awDep):
#         # call the initialization method of the Mixin class
#         super(AbstractWorkflowDependencyDataLog, self).__init__()
#         id = awDep.id
#         activity = awDep.activity
#         dependentActivity = awDep.dependentActivity
#
#
#     def __repr__(self):  # specifies how to display an AbstractWorkflowDependencyDataLog
#         return self.activity
#
#
# class ExpLineActDependencyDataLog(pyDatalog.Mixin):
#     def __init__(self, elaDep):
#         # call the initialization method of the Mixin class
#         super(ExpLineActDependencyDataLog, self).__init__()
#         id = elaDep.id
#         eLActivity = elaDep.eLActivity
#         dependentELActivity = elaDep.dependentELActivity
#         variant = elaDep.variant
#         optional = elaDep.optional
#
#
#     def __repr__(self):  # specifies how to display an ExpLineActDependencyDataLog
#         return self.eLActivity
#
#
# class InstantiationDataLog(pyDatalog.Mixin):
#     def __init__(self, instantiation):
#         # call the initialization method of the Mixin class
#         super(InstantiationDataLog, self).__init__()
#         abstractWorkflow = instantiation.abstractWorkflow
#         concreteWorkflow = instantiation.concreteWorkflow
#         abstractActivity = instantiation.abstractActivity
#         concreteActivity = instantiation.concreteActivity
#
#     def __repr__(self):  # specifies how to display an InstantiationDataLog
#         return self.abstractWorkflow
#
