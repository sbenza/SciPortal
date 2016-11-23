from django.conf.urls import url
from . import views
urlpatterns = [
url(r'^$', views.index_view, name='index'),
url(r'^(?P<explineid>[0-9]+)/$', views.expline_detail_view, name='detail'),
url(r'^(?P<explineid>[0-9]+)/derivations/$', views.expline_derivations_view, name='expLineDerivations'),
url(r'^addExpLine/$', views.add_expline, name='addExpLineView'),
# url(r'^addLine/$', views.addLine, name='addLine'),
url(r'^(?P<explineid>[0-9]+)/addELAct/$', views.add_ela_view, name='addELAct'),
url(r'^(?P<explineid>[0-9]+)/addAbstractWkf/$', views.add_abstract_workflow_view, name='addAbstractWkf'),
# url(r'^$', views.addAbstractWkfView, name='addAWkf'),
# url(r'^addELActivity/$', views.addELActivity, name='addELActivity'),
url(r'^(?P<explineid>[0-9]+)/addAbstractWkf/(?P<workflowid>[0-9]+)/$', views.add_abstract_activities_view, name='addWkfAct'),

]