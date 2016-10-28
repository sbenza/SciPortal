from django.shortcuts import render
from addline.aWkfForm import AbstractWorkflowForm
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
import json


def indexView(request):
    # ExpLineForm in the context of index but manage in the addExpLineView()
    latest_expline_list = ExpLine.objects.all()
    c = {'form': ExpLineForm(), 'latest_expline_list': latest_expline_list}
    return render(request, 'addline/index.html', c)


def addExpLineView(request):
    # get method not used anymore, the index renders the ExpLine form, didn't deleted just in case is usefull again
    if request.method == 'GET':
        c = {'form': ExpLineForm()}
        return render(request, 'addline/addExpLine.html', c)

    elif request.method == 'POST':
        #retrieve the posted data
        name = request.POST.get('name')
        description = request.POST.get('description')

        #save in the DB
        experiment = ExpLine(name=name, description=description)
        experiment.save()

        #store the response data to send to the html via json by the ajax code
        response_data = {}
        response_data['result'] = 'Add experiment successful!'
        response_data['expLineId'] = experiment.id
        response_data['expName'] = experiment.name

        #send the json to the html
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )


def expLineDetailView(request, explineid):
    try:
        expLine = ExpLine.objects.get(id=explineid)
        eLAct_list = ExpLineActivity.objects.filter(expLine=explineid)
        eLActDep_list = ExpLineActDependency.objects.filter(eLActivity__expLine__id=explineid)

        createGraph(eLAct_list, eLActDep_list, False)

        form = ELActivityForm(initial={'expLine': expLine})
        c = {'expLine': expLine, 'form': form, 'eLAct_list': eLAct_list, 'eLActDep_list': eLActDep_list, }

    except ExpLineActivity.DoesNotExist:
        raise Http404('ExpLineActivity not exist')
    # context = {'eLActDep_list': eLActDep_list, 'eLAct_list': eLAct_list, 'expLine': expLine}

    return render(request, 'addline/detail.html', c)


def addELANodes(graph, activities, editable):
    for activity in activities:
        if editable:
            graph.attr('node', href='/addline/editAbstractWkf/' + str(activity.id) + '/',
                       tooltip="click to edit this activity " + str(activity.id), fontsize='8.0')
        if activity.variant:
            if activity.optional:
                graph.node(name='ELA_' + str(activity.id), label=(activity.name + '\n<<' + activity.operation + '>>'),
                           shape='doubleoctagon', style='dashed', fontsize='8.0')
            else:
                graph.node(name='ELA_' + str(activity.id), label=(activity.name + '\n<<' + activity.operation + '>>'),
                           shape='doubleoctagon', fontsize='8.0')
                # , href="/addline/1/",
                # tooltip="click for the same place yet",fontsize='8.0')
        else:
            if activity.optional:
                graph.node(name='ELA_' + str(activity.id), label=(activity.name + '\n<<' + activity.operation + '>>'),
                           shape='egg', style='dashed', fontsize='8.0')
            else:
                graph.node(name='ELA_' + str(activity.id), label=(activity.name + '\n<<' + activity.operation + '>>'),
                           fontsize='8.0')


def addAbsActNodes(graph, derivations):
    sgraph = gv.Digraph('cluster_0')

    for activity in derivations:
        sgraph.node(name='AAct_' + str(activity.abstractActivity.id),
                    label=(activity.abstractActivity.name + '\n<<' + activity.abstractActivity.operation + '>>'),
                    shape='parallelogram', style='filled', fillcolor='grey', fontsize='6.0')

    graph.subgraph(sgraph)


def addAbsActEdges(graph, derivations):
    for activity in derivations:
        graph.edge('AAct_' + str(activity.abstractActivity.id), 'ELA_' + str(activity.expLineActivity.id), dir='none',
                   rank='same')


def addELAEdge(graph, dependencies):
    for dependency in dependencies:
        if dependency.variant:
            if dependency.optional:
                graph.edge('ELA_' + str(dependency.eLActivity.id), 'ELA_' + str(dependency.dependentELActivity.id),
                           style='dashed')
            else:
                graph.edge('ELA_' + str(dependency.eLActivity.id), 'ELA_' + str(dependency.dependentELActivity.id),
                           style='bold')
        else:
            if dependency.optional:
                graph.edge('ELA_' + str(dependency.eLActivity.id), 'ELA_' + str(dependency.dependentELActivity.id),
                           style='dashed')
            else:
                graph.edge('ELA_' + str(dependency.eLActivity.id), 'ELA_' + str(dependency.dependentELActivity.id))


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
        graph.attr('node', fontsize='8.0')

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


def addELActView(request, explineid):
    c = {}
    if request.method == 'GET':
        try:
            expLine = ExpLine.objects.get(id=explineid)
            eLAct_list = ExpLineActivity.objects.filter(expLine__id=explineid)
            form = ELActivityForm(initial={'expLine': expLine})

            c = {'expLine': expLine, 'form': form, 'eLAct_list': eLAct_list}
        except ExpLineActivity.DoesNotExist:
            raise Http404('ExpLineActivity not exist')

        return render(request, 'addline/addExpLineAct.html', c)

    elif request.method == 'POST':
        dependency = (request.POST.get('dependency')).split()
        name = request.POST.get('name')
        operation = request.POST.get('operation')
        variant = request.POST.get('variant')
        optional = request.POST.get('optional')
        expLine = ExpLine.objects.get(id=int(request.POST.get('id')))

        # save in the DB
        new_activity = ExpLineActivity(name=name, operation=operation, variant=variant, optional=optional,
                                       expLine=expLine)
        try:
            new_activity.save()
            if dependency != []:
                dep = []
                for item in dependency:
                    activity = ExpLineActivity.objects.get(id=int(item))
                    dep.append(ExpLineActDependency(eLActivity=activity, dependentELActivity=new_activity,
                                                    variant=activity.variant,
                                                    optional=activity.optional))
                    try:
                        dep[-1].full_clean()
                        continue
                    except:
                        new_activity.delete()
                for d in dep:
                    d.save()
        except:
            pass
        finally:
            eLAct_list = ExpLineActivity.objects.filter(expLine=explineid)
            eLActDep_list = ExpLineActDependency.objects.filter(eLActivity__expLine__id=explineid)
            createGraph(eLAct_list, eLActDep_list, False)

        #store the response data to send to the html via json by the ajax code
        response_data = {}

        #send the json to the html
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )


def addWkfAct(request, explineid,workflowid):
    # c = {'expLine': explineid}
    if request.method == 'POST':
         #retrieve the posted data
        # name = request.POST.get('name')
        # description = request.POST.get('description')
        #
        # #save in the DB
        # workflow = AbstractWorkflow(name=name, description=description)
        # workflow.save()
        #
        # #store the response data to send to the html via json by the ajax code
        response_data = {}
        # response_data['result'] = 'Add workflow successful!'
        # response_data['expLineId'] = explineid
        # response_data['wkfId'] = workflow.id
        # response_data['wkfName'] = workflow.name

        #send the json to the html
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

    elif request.method == 'GET':
        try:
            expLine = ExpLine.objects.get(id=explineid)
            workflow = AbstractWorkflow.objects.get(id=workflowid)
            eLAct_list = ExpLineActivity.objects.filter(expLine=explineid)
            aAct_list = AbstractActivity.objects.filter(derivation__expLineActivity__expLine__id=explineid)
            eLActDep_list = ExpLineActDependency.objects.filter(eLActivity__expLine__id=explineid)
            aActDep_list = AbstractWorkflowDependency.objects.filter(activity__expLineActivity__expLine__id=explineid)
            # graph = createGraph(eLAct_list, eLActDep_list, True)

            derivations_list = Derivation.objects.filter(expLineActivity__expLine_id=explineid)
            abstractActDep_list = AbstractWorkflowDependency.objects.filter(
                activity__expLineActivity__expLine__id=explineid)

            createSubGraph(derivations_list, abstractActDep_list)
            form = AbstractWorkflowForm()
        except ExpLineActivity.DoesNotExist:
            raise Http404('ExpLineActivity not exist')

        c = {'workflow': workflow, 'eLAct_list': eLAct_list, 'eLActDep_list':eLActDep_list, 'expLine': expLine,  'aAct_list':aAct_list, 'aActDep_list':aActDep_list, 'form': form}

        return render(request, 'addline/workflow.html', c)


def manageAbstractWkfView(request, explineid):
    c = {'expLine': explineid}
    if request.method == 'POST':
         #retrieve the posted data
        name = request.POST.get('name')
        description = request.POST.get('description')

        #save in the DB
        workflow = AbstractWorkflow(name=name, description=description)
        workflow.save()

        #store the response data to send to the html via json by the ajax code
        response_data = {}
        response_data['result'] = 'Add workflow successful!'
        response_data['expLineId'] = explineid
        response_data['wkfId'] = workflow.id
        response_data['wkfName'] = workflow.name

        #send the json to the html
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

    elif request.method == 'GET':
        try:
            expLine = ExpLine.objects.get(id=explineid)
            eLAct_list = ExpLineActivity.objects.filter(expLine=explineid)
            eLActDep_list = ExpLineActDependency.objects.filter(eLActivity__expLine__id=explineid)
            workflow_list = AbstractWorkflow.objects.filter(expLine__id=explineid)
            # graph = createGraph(eLAct_list, eLActDep_list, True)

            derivations_list = Derivation.objects.filter(expLineActivity__expLine_id=explineid)
            abstractActDep_list = AbstractWorkflowDependency.objects.filter(
                activity__expLineActivity__expLine__id=explineid)

            createSubGraph(derivations_list, abstractActDep_list)
            form = AbstractWorkflowForm()
        except ExpLineActivity.DoesNotExist:
            raise Http404('ExpLineActivity not exist')

        c = {'eLActDep_list': eLActDep_list, 'eLAct_list': eLAct_list, 'expLine': expLine, 'workflow_list' : workflow_list, 'form': form}

        return render(request, 'addline/addAbstractWkf.html', c)