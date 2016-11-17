import json

# import graphviz as gv
from pygraphviz import *
from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse

from addline.aWkfForm import AbstractWorkflowForm
from addline.eLActivityForm import ELActivityForm
from addline.expLineForm import *
from addline.dataLogFunctions import *


# Create your views here.

def indexView(request):
    try:
        # t = teste() #testando o pydatalog
        # ExpLineForm in the context of index but manage in the addExpLineView()
        latest_expline_list = ExpLine.objects.all()
        c = {'form': ExpLineForm(), 'latest_expline_list': latest_expline_list,
        }
    except ExpLineActivity.DoesNotExist:
        raise Http404('ExpLineActivity not exist')

    return render(request, 'addline/index.html', c)




def addExpLine(request):
    # get method not used anymore, the index renders the ExpLine form, didn't deleted just in case is usefull again
    if request.method == 'GET':
        c = {'form': ExpLineForm()}
        return render(request, 'addline/addExpLine.html', c)

    elif request.method == 'POST':
        # retrieve the posted data
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
        abstractAct_list = Derivation.objects.filter(expLineActivity__expLine=explineid)
        abstractActDep_list = AbstractWorkflowDependency.objects.filter(
            activity__expLineActivity__expLine__id=explineid)

        createSubGraph(abstractAct_list, abstractActDep_list)
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
                graph.add_node(n= str(activity.id), label=(activity.name + '\n' + activity.operation),
                           shape='doubleoctagon', style='dashed', fontsize='8.0')
            else:
                graph.add_node(n= str(activity.id), label=(activity.name + '\n' + activity.operation),
                           shape='doubleoctagon', fontsize='8.0')
                # , href="/addline/1/",
                # tooltip="click for the same place yet",fontsize='8.0')
        else:
            if activity.optional:
                graph.add_node(n=str(activity.id), label=(activity.name + '\n' + activity.operation ),
                           shape='egg', style='dashed', fontsize='8.0')
            else:
                graph.add_node(n= str(activity.id), label=(activity.name + '\n' + activity.operation ),
                           fontsize='8.0')


def addAbsActNodes(graph, derivations):
    sgraph = gv.Digraph('cluster_0')

    for activity in derivations:
        sgraph.node(name= str(activity.abstractActivity.id),
                    label=(activity.abstractActivity.name + '\n' + activity.abstractActivity.operation ),
                    shape='parallelogram', style='filled', fillcolor='grey', fontsize='6.0')

    graph.subgraph(sgraph)


def addAbsActEdges(graph, derivations):
    for activity in derivations:
        graph.edge( str(activity.abstractActivity.id),   str(activity.expLineActivity.id), dir='none',
                   rank='same')


def addELAEdge(graph, dependencies):
    for dependency in dependencies:
        if dependency.variant:
            if dependency.optional:
                graph.add_edge( str(dependency.eLActivity.id), str(dependency.dependentELActivity.id),
                           style='dashed')
            else:
                graph.add_edge(str(dependency.eLActivity.id),str(dependency.dependentELActivity.id),
                           style='bold')
        else:
            if dependency.optional:
                graph.add_edge(str(dependency.eLActivity.id),  str(dependency.dependentELActivity.id),
                           style='dashed')
            else:
                graph.add_edge(str(dependency.eLActivity.id), str(dependency.dependentELActivity.id))


def createGraph(activities, dependencies, editable):
    graph = AGraph(strict=False,directed=True)
    addELANodes(graph, activities, editable)

    addELAEdge(graph, dependencies)

    graph.layout(prog='dot')

    graph.draw(path='addline/templates/svg/expline.svg',format='svg')

    return graph


def createSubGraph(activities, dependencies):
    graph = AGraph(strict=False,directed=True)

    for activity in activities:
        graph.add_node(n=str(activity.id), label=(
                activity.abstractActivity.name + '\n' + activity.abstractActivity.operation ),fontsize='8.0')
    for dependency in dependencies:
        graph.add_edge(str(dependency.activity.id), str(dependency.dependentActivity.id))
    graph.layout('dot')

    graph.draw(path='addline/templates/svg/derivations.svg',format='svg')


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
    response_data={'text': 'Valid Experiment Line, you can derive an Abstract Workflow now =D', 'cardinality_text':''}
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


        try:
            # update the DB
            new_activity = ExpLineActivity(name=name, operation=operation, variant=variant, optional=optional,
                                       expLine=expLine)
            new_activity.save()
            if dependency:
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
                        raise Http404('New activity not saved')

                for d in dep:
                    d.save()
        except:
            raise Http404('New activity not saved')
        finally:
            eLAct_list = ExpLineActivity.objects.filter(expLine=explineid)
            eLActDep_list = ExpLineActDependency.objects.filter(eLActivity__expLine__id=explineid)
            createGraph(eLAct_list, eLActDep_list, False)
            print ('grafo atualizado')

        # store the response data to send to the html via json by the ajax code
        response_data = {}

        #send the json to the html
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    elif request.method == 'PUT':
        try:
           # todo LOGIC
            eLAct_list = ExpLineActivity.objects.filter(expLine=explineid)
            eLActDep_list = ExpLineActDependency.objects.filter(eLActivity__expLine__id=explineid)

        except:
            pass
        finally:
            # eLAct_list = ExpLineActivity.objects.filter(expLine=explineid)
            # eLActDep_list = ExpLineActDependency.objects.filter(eLActivity__expLine__id=explineid)
            graph= createGraph(eLAct_list, eLActDep_list, False)
            cardinality=check_cardinality(graph,eLActDep_list)
            conectivity = check_connectivity(graph)
            # print ('grafo atualizado')
            # store the response data to send to the html via json by the ajax code

        if cardinality:
            response_data={'text':'Invalid Experiment','cardinality_text':cardinality}
        if conectivity :
            response_data['text'] = conectivity[0]+'<br>'+str(conectivity[1])
        # print (response_data)
        #send the json to the html
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

def derivationManagementView(request, explineid, workflowid):
    # c = {'expLine': explineid}
    if request.method == 'POST':
        # retrieve the posted data
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
            # eLAct_list = ExpLineActivity.objects.filter(expLine=explineid)
            # aAct_list = AbstractActivity.objects.filter(derivation__expLineActivity__expLine__id=explineid)
            # eLActDep_list = ExpLineActDependency.objects.filter(eLActivity__expLine__id=explineid)
            # aActDep_list = AbstractWorkflowDependency.objects.filter(activity__expLineActivity__expLine__id=explineid)
            # graph = createGraph(eLAct_list, eLActDep_list, True)
            # form = AbstractWorkflowForm()

            activities = {}
            derivations_list = Derivation.objects.filter(expLineActivity__expLine_id=explineid).filter(
                abstractWorkflow__id=workflowid)

            for derivation in derivations_list:
                activities[derivation.abstractActivity] = []
                dependencies = AbstractWorkflowDependency.objects.filter(dependentActivity=derivation)
                for dependency in dependencies:
                    activities[derivation.abstractActivity].append(dependency.activity.abstractActivity)

            activities_items = activities.items()
            activities_list = []
            keys = []

            for k, v in activities_items:
                if v != []:
                    vList = []
                    for item in v:
                        vList.append(item.name)
                    string = (k.name + '. Dependency: ' + ', '.join(vList))
                else:
                    string = k.name + '. No Dependency'
                    keys.append(k)

                activities_list.append((string))

            restrictedAct_list = activities
            for k in keys:
                restrictedAct_list.pop(k)




        except ExpLineActivity.DoesNotExist:
            raise Http404('ExpLineActivity not exist')
        #
        # c = {'workflow': workflow, 'eLAct_list': eLAct_list, 'eLActDep_list':eLActDep_list, 'expLine': expLine,
        # 'aAct_list':aAct_list, 'aActDep_list':aActDep_list, 'activities': activities_list,'form': form}

        c = {'expLine': expLine, 'activities': activities_list, 'restrictedAct_list': restrictedAct_list,
             'availableAct_list': keys, 'workflow': workflow}

        return render(request, 'addline/derivationManagement.html', c)


def abstractWkfManagementView(request, explineid):
    c = {'expLine': explineid}
    if request.method == 'POST':
        # retrieve the posted data
        name = request.POST.get('name')
        description = request.POST.get('description')
        expLine = ExpLine(id=explineid)
        #save in the DB
        workflow = AbstractWorkflow(name=name, description=description, expLine=expLine)
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

            # createSubGraph(derivations_list, abstractActDep_list)
            form = AbstractWorkflowForm()
        except ExpLineActivity.DoesNotExist:
            raise Http404('ExpLineActivity not exist')

        c = {'eLActDep_list': eLActDep_list, 'eLAct_list': eLAct_list, 'expLine': expLine,
             'workflow_list': workflow_list, 'form': form}

        return render(request, 'addline/addAbstractWkf.html', c)