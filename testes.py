#copy paste
def execfile(file):
    with open(file) as source_file:
        exec(source_file.read())
        
#then run        
#('testes.py')        
        
import django
django.setup()
from pyDatalog import pyDatalog
from django.db import models
from addline.models import *
exp=ExpLine.objects.all()
pyDatalog.create_terms('X,Y,experiment,Activity')
# act=ExpLineActivity.objects.all()
# X.in_(exp)
# print (X.in_(exp))
# X.name
# experiment[exp[0]]=exp[0].name
# experiment[exp[1]]=exp[1].name
# experiment[exp[2]]=exp[2].name
# experiment[exp[3]]=exp[3].name
# print(experiment[X]==Y)
# print ('\n')
# print (exp[0]==Y)





    
#vem da view
explineid=3

#extraido do views, models
expLine = ExpLine.objects.get(id=explineid)
eLAct_list = ExpLineActivity.objects.filter(expLine=explineid)
eLActDep_list = ExpLineActDependency.objects.filter(eLActivity__expLine__id=explineid)
abstractAct_list = Derivation.objects.filter(expLineActivity__expLine=explineid)
abstractActDep_list = AbstractActivityDependency.objects.filter(
    activity__expLineActivity__expLine__id=explineid)

print (expLine.id)