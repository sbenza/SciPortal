from django.shortcuts import render
# from addline.depELAForm import DepELAForm
from addline.eLActivityForm import ELActivityForm
from addline.expLineForm import ExpLineForm
from addline.models import *
from django.http import Http404, HttpResponseRedirect
from django.contrib import messages

from django.template import loader
# Create your views here.

from django.http import HttpResponse
from django.urls import reverse
import graphviz as gv
import pygraphviz as pgv


def indexView(request):
    latest_expline_list = ExpLine.objects.all()
    context = {'latest_expline_list': latest_expline_list}
    return render(request, 'addline/index.html', context)


def expLineDetailView(request, explineid):
    try:
        # recupera dados do expLine e das atividades do expLine
        expLine = ExpLine.objects.get(id=explineid)
        eLAct_list = ExpLineActivity.objects.filter(expLine=explineid)
        eLActDep_list = ExpLineActDependency.objects.filter(eLActivity__expLine__id=explineid)

        createGraph(eLAct_list, eLActDep_list,False)

    except ExpLineActivity.DoesNotExist:
        raise Http404('ExpLineActivity not exist')
    context = {'eLActDep_list': eLActDep_list, 'eLAct_list': eLAct_list, 'expLine': expLine}

    return render(request, 'addline/detail.html', context)
    # return HttpResponse('this is the expline: %s' % expline.)


def addELANodes(graph, activities, editable):
    for activity in activities:
        if editable:
            graph.attr('node', href = '/addline/editAbstractWkf/' + str(activity.id)+'/', tooltip="click to edit this activity " + str(activity.id), fontsize= '8.0')
        if activity.variant:
            if activity.optional:
                graph.node(name='ELA_'+str(activity.id), label=(activity.name + '\n<<' + activity.operation + '>>'),
                           shape='doubleoctagon', style='dashed')
            else:
                graph.node(name='ELA_'+str(activity.id), label=(activity.name + '\n<<' + activity.operation + '>>'),
                           shape='doubleoctagon')
                # , href="/addline/1/",
                # tooltip="click for the same place yet")
        else:
            if activity.optional:
                graph.node(name='ELA_'+str(activity.id), label=(activity.name + '\n<<' + activity.operation + '>>'),
                           shape='egg', style='dashed')
            else:
                graph.node(name='ELA_'+str(activity.id), label=(activity.name + '\n<<' + activity.operation + '>>'))


def addAbsActNodes(graph, derivations):
    sgraph = gv.Digraph('cluster_0')

    for activity in derivations:
        sgraph.node(name='AAct_'+str(activity.abstractActivity.id), label=(activity.abstractActivity.name + '\n<<' + activity.abstractActivity.operation + '>>'), shape='parallelogram', style='filled', fillcolor='grey', fontsize='6.0')

    graph.subgraph(sgraph)

def addAbsActEdges(graph, derivations):
    for activity in derivations:
        graph.edge( 'AAct_'+str(activity.abstractActivity.id),'ELA_'+str(activity.expLineActivity.id), dir='none', rank='same')


def addELAEdge(graph, dependencies):
    for dependency in dependencies:
        if dependency.variant:
            if dependency.optional:
                graph.edge('ELA_'+str(dependency.eLActivity.id), 'ELA_'+str(dependency.dependentELActivity.id), style='dashed')
            else:
                graph.edge('ELA_'+str(dependency.eLActivity.id), 'ELA_'+str(dependency.dependentELActivity.id), style='bold')
        else:
            if dependency.optional:
                graph.edge('ELA_'+str(dependency.eLActivity.id), 'ELA_'+str(dependency.dependentELActivity.id), style='dashed')
            else:
                graph.edge('ELA_'+str(dependency.eLActivity.id), 'ELA_'+str(dependency.dependentELActivity.id))


def createGraph(activities, dependencies, editable):
    graph = gv.Digraph(format='svg')
    addELANodes(graph, activities, editable)

    addELAEdge(graph, dependencies)

    graph.render(filename='addline/templates/svg/expline')

    # print(g1)

    return graph


def createSubGraph(activities, dependencies):
    graph = gv.Digraph(format='svg')
    graphDict = {}

    for activity in activities:
        graph.attr('node', fontsize= '8.0')

        if activity.abstractWorkflow.id not in graphDict:
            graphDict[activity.abstractWorkflow.id] = gv.Digraph('cluster_' + str(activity.abstractWorkflow.id))
            graphDict[activity.abstractWorkflow.id].body.append('label=' + activity.abstractWorkflow.name)
            graphDict[activity.abstractWorkflow.id].node(name=str(activity.id), label=(
                activity.abstractActivity.name + '\n<<' + activity.abstractActivity.operation + '>>'))
        else:
            graphDict[activity.abstractWorkflow.id].node(name=str(activity.id), label=(
                activity.abstractActivity.name + '\n<<' + activity.abstractActivity.operation + '>>'))

    for subGraph in graphDict.items():
        graph.subgraph(subGraph[1])

    for dependency in dependencies:
        graph.edge(str(dependency.activity.id), str(dependency.dependentActivity.id))

    graph.render(filename='addline/templates/svg/derivations')


def expLineDerivationsView(request, explineid):
    try:
        # recupera dados do expLine e das atividades do expLine
        expLine = ExpLine.objects.get(id=explineid)
        abstractAct_list = Derivation.objects.filter(expLineActivity__expLine=explineid)
        abstractActDep_list = AbstractWorkflowDependency.objects.filter(
            activity__expLineActivity__expLine__id=explineid)

        createSubGraph(abstractAct_list, abstractActDep_list)

    except ExpLineActivity.DoesNotExist:
        raise Http404('ExpLineActivity not exist')
    context = {'abstractActDep_list': abstractActDep_list, 'abstractAct_list': abstractAct_list, 'expLine': expLine}

    return render(request, 'addline/derivations.html', context)


def addExpLineView(request):
    c = {}
    if request.method == 'GET':

        c = {'form': ExpLineForm()}

        return render(request, 'addline/addExpLine.html', c)

    elif request.method == 'POST':
        form = ExpLineForm(request.POST)
        if form.is_valid():
            experiment = form.save()
        else:
            c['form'] = form
            return render(request, 'addline/addExpLine.html', c)

        return HttpResponseRedirect(reverse('addline:detail', args=(experiment.id,)))


def addELActView(request, explineid):
    c={}
    if request.method == 'GET':


        try:
            expLine = ExpLine.objects.get(id=explineid)
            eLAct_list = ExpLineActivity.objects.filter(expLine__id=explineid)
            form = ELActivityForm(initial={'expLine': expLine})
            # formDep = DepELAForm(initial={'explineid':expLine.id})
            # formDep = DepELAForm()

            c = {'expLine': expLine, 'form': form,  'eLAct_list':eLAct_list}
        except ExpLineActivity.DoesNotExist:
            raise Http404('ExpLineActivity not exist')

        return render(request, 'addline/addExpLineAct.html', c)

    elif request.method == 'POST':
        form = ELActivityForm(request.POST)
        # dep= ExpLineActDependency()
        # formDep = DepELAForm(request.POST, instance=dep)
        dependency = request.POST.getlist('dependency')
        # A= formDep.is_valid()
        if form.is_valid():
            new_activity = form.save()

            if dependency != []:
                dep=[]
                for item in dependency:
                    activity = ExpLineActivity.objects.get(id=int(item))
                    dep.append(ExpLineActDependency(eLActivity=activity, dependentELActivity=new_activity, variant=activity.variant,
                                               optional=activity.optional))
                    try:
                        dep[-1].full_clean()
                        continue
                    except:
                        new_activity.delete()


                # formDep.clean_data['eLActivity':activity]
                for d in dep: d.save()
        else:
            expLine = ExpLine.objects.get(id=explineid)
            eLAct_list = ExpLineActivity.objects.filter(expLine__id=explineid)
            form = ELActivityForm(initial={'expLine': expLine})
            # formDep = DepELAForm(initial={'explineid':expLine.id},
            #                      # 'eLActivity'=form.
            # )


            c = {'expLine': expLine,  'form': form, 'eLAct_list':eLAct_list}
            return render(request, 'addline/addExpLineAct.html', c)

        return HttpResponseRedirect(reverse('addline:detail', args=(explineid,)))


def addAbstractWkfView(request, explineid):
    c = {}
    if request.method == 'GET':
        try:
            expLine = ExpLine.objects.get(id=explineid)
            eLAct_list = ExpLineActivity.objects.filter(expLine=explineid)
            eLActDep_list = ExpLineActDependency.objects.filter(eLActivity__expLine__id=explineid)

            graph= createGraph(eLAct_list, eLActDep_list, True)

            derivations_list = Derivation.objects.filter(expLineActivity__expLine=explineid)
            abstractActDep_list = AbstractWorkflowDependency.objects.filter(activity__expLineActivity__expLine__id=explineid)
            #
            # addAbsActNodes(graph, derivations_list)
            # addAbsActEdges(graph, derivations_list)
            # graph.render(filename='addline/templates/svg/expline')

            createSubGraph(derivations_list, abstractActDep_list)

        except ExpLineActivity.DoesNotExist:
            raise Http404('ExpLineActivity not exist')

        c = {'eLActDep_list': eLActDep_list, 'eLAct_list': eLAct_list, 'expLine': expLine}



        return render(request, 'addline/addAbstractWkf.html', c)

    elif request.method == 'POST':

        form = ExpLineForm(request.POST)
        if form.is_valid():
            experiment = form.save()
        else:
            c['form'] = form
            return render(request, 'addline/addExpLine.html', c)

        return HttpResponseRedirect(reverse('addline:detail', args=(experiment.id,)))
