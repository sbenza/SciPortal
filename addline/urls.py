from django.conf.urls import url
from . import views
urlpatterns = [
url(r'^$', views.indexView, name='index'),
url(r'^(?P<explineid>[0-9]+)/$', views.expLineDetailView, name='detail'),
url(r'^(?P<explineid>[0-9]+)/derivations/$', views.expLineDerivationsView, name='expLineDerivations'),
url(r'^addExpLine/$', views.addExpLineView, name='addExpLineView'),
# url(r'^addLine/$', views.addLine, name='addLine'),
url(r'^(?P<explineid>[0-9]+)/addELAct/$', views.addELActView, name='addELAct'),
url(r'^(?P<explineid>[0-9]+)/addAbstractWkf/$', views.manageAbstractWkfView, name='addAbstractWkf'),
# url(r'^$', views.addAbstractWkfView, name='addAWkf'),
# url(r'^addELActivity/$', views.addELActivity, name='addELActivity'),
url(r'^(?P<explineid>[0-9]+)/addAbstractWkf/(?P<workflowid>[0-9]+)/$', views.addWkfAct, name='addWkfAct'),

]