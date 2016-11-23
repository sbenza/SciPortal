import json

# import graphviz as gv
from pygraphviz import *
from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from django.http import QueryDict
from django.core import serializers

from addline.aWkfForm import AbstractWorkflowForm
from addline.absActivityForm import AbstractActivityForm
from addline.eLActivityForm import ELActivityForm
from addline.expLineForm import *
from addline.dataLogFunctions import *


# Create your views here.

def index_view(request):
    try:
        # t = teste() #testando o pydatalog
        # ExpLineForm in the context of index but manage in the addExpLineView()
        latest_expline_list = ExpLine.objects.all()
        c = {'form': ExpLineForm(), 'latest_expline_list': latest_expline_list,
        }
    except ExpLineActivity.DoesNotExist:
        raise Http404('ExpLineActivity not exist')

    return render(request, 'addline/index.html', c)


def add_expline(request):
    # get method not used anymore, the index renders the ExpLine form, didn't deleted just in case is usefull again
    if request.method == 'GET':
        c = {'form': ExpLineForm()}
        return render(request, 'addline/addExpLine.html', c)

    # refactoring needed, post method should be in index_view function!
    elif request.method == 'POST':
        # retrieve the posted data
        name = request.POST.get('name')
        description = request.POST.get('description')

        # save in the DB
        experiment = ExpLine(name=name, description=description)
        experiment.save()

        # store the response data to send to the html via json by the ajax code
        response_data = {'result': 'Add experiment successful!',
                         'expLineId': experiment.id,
                         'expName': experiment.name
        }

        # send the json to the html
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )


def expline_detail_view(request, explineid):
    try:
        expLine = ExpLine.objects.get(id=explineid)
        eLAct_list = ExpLineActivity.objects.filter(expLine=explineid)
        eLActDep_list = ExpLineActDependency.objects.filter(eLActivity__expLine__id=explineid)

        create_graph(eLAct_list, eLActDep_list, False)
        abstractAct_list = Derivation.objects.filter(expLineActivity__expLine=explineid)
        abstractActDep_list = AbstractActivityDependency.objects.filter(
            activity__expLineActivity__expLine__id=explineid)

        create_subgraph(abstractAct_list, abstractActDep_list, 'derivations')
        form = ELActivityForm(initial={'expLine': expLine})

        c = {'expLine': expLine, 'form': form, 'eLAct_list': eLAct_list, 'eLActDep_list': eLActDep_list, }

    except ExpLineActivity.DoesNotExist:
        raise Http404('ExpLineActivity not exist')

    return render(request, 'addline/detail.html', c)


def add_ela_nodes(graph, activities, editable=False, href=""):
    for activity in activities:

        if activity.variant:
            if activity.optional:
                graph.add_node(n=str(activity.id), label=(activity.name + '\n' + activity.operation),
                               shape='doubleoctagon', style='dashed', fontsize='7.0')
            else:
                graph.add_node(n=str(activity.id), label=(activity.name + '\n' + activity.operation),
                               shape='doubleoctagon', fontsize='7.0')
                # , href="/addline/1/",
                # tooltip="click for the same place yet",fontsize='8.0')
        else:
            if activity.optional:
                graph.add_node(n=str(activity.id), label=(activity.name + '\n' + activity.operation ),
                               shape='egg', style='dashed', fontsize='7.0')
            else:
                graph.add_node(n=str(activity.id), label=(activity.name + '\n' + activity.operation ),
                               fontsize='7.0')
        if editable:
            node = graph.get_node(str(activity.id))
            node.attr['href'] = '/' + href + str(activity.id) + '/'
            node.attr['tooltip'] = "click to manage this activity " + str(activity.id)
            # href = '/addline/editAbstractWkf/'


def add_ela_edges(graph, dependencies):
    for dependency in dependencies:
        if dependency.variant:
            if dependency.optional:
                graph.add_edge(str(dependency.eLActivity.id), str(dependency.dependentELActivity.id),
                               style='dashed')
            else:
                graph.add_edge(str(dependency.eLActivity.id), str(dependency.dependentELActivity.id),
                               style='bold')
        else:
            if dependency.optional:
                graph.add_edge(str(dependency.eLActivity.id), str(dependency.dependentELActivity.id),
                               style='dashed')
            else:
                graph.add_edge(str(dependency.eLActivity.id), str(dependency.dependentELActivity.id))


def create_graph(activities, dependencies, editable=False, href=""):
    graph = AGraph(strict=False, directed=True)
    add_ela_nodes(graph, activities, editable, href)

    add_ela_edges(graph, dependencies)

    graph.layout(prog='dot')

    graph.draw(path='addline/templates/svg/expline.svg', format='svg')

    return graph


def create_subgraph(activities, dependencies, name):
    graph = AGraph(strict=False, directed=True)

    for activity in activities:
        graph.add_node(n=str(activity.id), label=(
            activity.abstractActivity.name + '\n' + activity.abstractActivity.operation ), fontsize='8.0')
    for dependency in dependencies:
        graph.add_edge(str(dependency.activity.id), str(dependency.dependentActivity.id))
    graph.layout('dot')

    graph.draw(path='addline/templates/svg/' + name + '.svg', format='svg')


def expline_derivations_view(request, explineid):
    try:
        # recupera dados do expLine e das atividades do expLine
        expLine = ExpLine.objects.get(id=explineid)
        abstractAct_list = Derivation.objects.filter(expLineActivity__expLine=explineid)
        abstractActDep_list = AbstractActivityDependency.objects.filter(
            activity__expLineActivity__expLine__id=explineid)

        create_subgraph(abstractAct_list, abstractActDep_list, 'derivations')

    except ExpLineActivity.DoesNotExist:
        raise Http404('ExpLineActivity not exist')
    context = {'abstractActDep_list': abstractActDep_list, 'abstractAct_list': abstractAct_list, 'expLine': expLine}

    return render(request, 'addline/derivations.html', context)


def check_expline(explineid, response_data):
    eLAct_list = ExpLineActivity.objects.filter(expLine=explineid)
    eLActDep_list = ExpLineActDependency.objects.filter(eLActivity__expLine__id=explineid)
    graph = create_graph(eLAct_list, eLActDep_list, False)
    cardinality = check_cardinality(graph, eLActDep_list)
    conectivity = check_connectivity(graph)
    if cardinality:
        response_data = {'text': 'Invalid Experiment', 'cardinality_text': cardinality}
    if conectivity:
        response_data['text'] = conectivity[0] + '<br>' + str(conectivity[1])
    return response_data


def add_ela_view(request, explineid):
    response_data = {'text': 'Valid Experiment Line, you can derive an Abstract Workflow now =D',
                     'cardinality_text': ''}
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
            create_graph(eLAct_list, eLActDep_list, False)
            print('grafo atualizado')

        # store the response data to send to the html via json by the ajax code
        response_data = {}

        # send the json to the html
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    elif request.method == 'PUT':
        try:
            response_data = check_expline(explineid, response_data)

        except:
            pass

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )


def draw_editable_elas(explineid, graph):
    eLAct_list = ExpLineActivity.objects.filter(expLine=explineid)
    add_ela_nodes(graph, eLAct_list, True)
    # add editable feature to node
    for activity in eLAct_list:
        graph.add_node(n=str(activity.id),
                       # label=(activity.name + '\n(' + activity.operation + ')'),
                       # fontsize='7.0',
                       href='javascript:openForm(' + str(activity.id) + ');',
                       tooltip="click to manage this activity " + str(activity.name)
        )

    graph.layout(prog='dot')
    graph.draw(path='addline/templates/svg/editable_graph.svg', format='svg')


def add_abstract_activities_view(request, explineid, workflowid):
    # c = {'expLine': explineid}
    response_data = {'text': 'Valid Workflow Line, you can Instantiate a Concrete Workflow now =D',
                     'cardinality_text': ''}
    if request.method == 'POST':
        if request.POST.get('func') == 'selectAA':
            # retriving infos from post
            selected_activities_list = (request.POST.get('activities')).split()
            ela_id = request.POST.get('elaid')
            wkf_id = request.POST.get('workflowid')

            # get ela (helps to check if the activity is dependent, via expline)
            ela = ExpLineActivity.objects.get(id=int(ela_id))

            # get wokflow object
            workflow = AbstractWorkflow.objects.get(id=int(wkf_id))

            #get all objects activities selected to add to the derived workflow
            activities = []
            for i in selected_activities_list:
                activities.append(AbstractActivity.objects.get(id=int(i)))

            #get all activities (if any) tha are the dependencies of the actual ela
            try:
                elaDep = ExpLineActDependency.objects.filter(dependentELActivity=ela)
            except:
                elaDep = []

            #
            derivation_dependency_list = []
            for i in elaDep:
                if i.eLActivity.optional == False:
                    # print (i)
                    dependency = Derivation.objects.filter(abstractWorkflow=workflow).filter(
                        expLineActivity__eLActivity=i)
                    derivation_dependency_list.append(dependency)
                    if not dependency:
                        response_data = {
                            'text': 'This activity has a Mandatory ELA dependency not covered yet: ' + i.eLActivity.name}
                        # print(response_data)
                        return HttpResponse(
                            json.dumps(response_data),
                            content_type="application/json")


            #for each activity selected add to the derived workflow, if it wasn't added yed
            # (temporary until create the error to user or block)
            derivation_list = []
            for i in activities:
                try:
                    Derivation.objects.get(expLineActivity=ela, abstractWorkflow=workflow,
                                           abstractActivity=i)
                    response_data = {'text': 'Activity already in the workflow'}
                    return HttpResponse(
                        json.dumps(response_data),
                        content_type="application/json")
                except:
                    derivation = Derivation(expLineActivity=ela, abstractWorkflow=workflow, abstractActivity=i)
                    derivation.save()
                    derivation_list.append(derivation)

            for derivation_dependency in derivation_dependency_list:
                for activity in derivation_dependency:
                    for dependent_activity in derivation_list:
                        new_dependency = AbstractActivityDependency(activity=activity,
                                                                    dependentActivity=dependent_activity)
                        print(new_dependency.activity.id, new_dependency.dependentActivity.id)
                        new_dependency.save()

            #draw updated derived workflow
            abstract_act_list = Derivation.objects.filter(abstractWorkflow=workflow)
            abstract_act_dep_list = AbstractActivityDependency.objects.filter(activity__abstractWorkflow=workflow)
            create_subgraph(abstract_act_list, abstract_act_dep_list, 'workflow')

            response_data = {'text': ''}
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json")

        elif request.POST.get('func') == 'checkWkf':

            response_data = check_expline(explineid, response_data)
            workflowid

            #check if every mandatory ela has an AA in the wf
            ela_list = ExpLineActivity.objects.filter(expLine_id=explineid).filter(optional=False)
            abstract_act_list = Derivation.objects.filter(abstractWorkflow_id=workflowid)
            wkf_elas=[]
            for activity in abstract_act_list:
                if activity.expLineActivity in ela_list and activity.expLineActivity.name not in wkf_elas:
                    wkf_elas.append(activity.expLineActivity.name)
                    print (activity.expLineActivity.name,wkf_elas)
            print (len(ela_list) , len(wkf_elas))
            if len(ela_list) != len(wkf_elas):
                response_data['text']= 'Not valid, more mandatory activities needed to close the Experiment Line'

        else:
            # todo new AA, already retrieving the posted data
            name = request.POST.get('name')
            description = request.POST.get('description')
            print(name, description)

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

    elif request.method == 'GET':
        try:
            expLine = ExpLine.objects.get(id=explineid)
            eLAct_list = ExpLineActivity.objects.filter(expLine=explineid)
            eLActDep_list = ExpLineActDependency.objects.filter(eLActivity__expLine__id=explineid)
            graph = create_graph(eLAct_list, eLActDep_list)
            draw_editable_elas(explineid, graph)

            workflow = AbstractWorkflow.objects.get(id=workflowid)
            abstract_act_list = Derivation.objects.filter(abstractWorkflow=workflow)
            abstract_act_dep_list = AbstractActivityDependency.objects.filter(activity__abstractWorkflow=workflow)
            create_subgraph(abstract_act_list, abstract_act_dep_list, 'workflow')


            # activities = {}
            # derivations_list = Derivation.objects.filter(expLineActivity__expLine_id=explineid).filter(
            # abstractWorkflow__id=workflowid)
            #
            # for derivation in derivations_list:
            # activities[derivation.abstractActivity] = []
            # dependencies = AbstractWorkflowDependency.objects.filter(dependentActivity=derivation)
            #     for dependency in dependencies:
            #         activities[derivation.abstractActivity].append(dependency.activity.abstractActivity)
            #
            # activities_items = activities.items()
            # activities_list = []
            # keys = []
            #
            # for k, v in activities_items:
            #     if v != []:
            #         vList = []
            #         for item in v:
            #             vList.append(item.name)
            #         string = (k.name + '. Dependency: ' + ', '.join(vList))
            #     else:
            #         string = k.name + '. No Dependency'
            #         keys.append(k)
            #
            #     activities_list.append((string))
            #
            # restrictedAct_list = activities
            # for k in keys:
            #     restrictedAct_list.pop(k)

        except ExpLineActivity.DoesNotExist:
            raise Http404('ExpLineActivity not exist')

        c = {
            'expLine': expLine,
            'abstractAct_list': abstract_act_list,
            # 'restrictedAct_list': restrictedAct_list,
            # 'availableAct_list': keys,
            'workflow': workflow,
            'form': AbstractActivityForm()
        }

        return render(request, 'addline/derivationManagement.html', c)
    elif request.method == 'PUT':
        put = QueryDict(request.body)
        ela_id = put.get('id')

        # get list of derivations of selected ela (i.e. to get activities already derived in other wkfs)
        selected_activities_list = Derivation.objects.filter(expLineActivity=ela_id).distinct('abstractActivity')

        # create list of available abstract activities of selected ela
        aa_list = []
        for i in selected_activities_list:
            aa_list.append((i.abstractActivity))

        response_data = (serializers.serialize("json", aa_list))

        return HttpResponse(
            (response_data),
            content_type="application/json"
        )


def add_abstract_workflow_view(request, explineid):
    if request.method == 'POST':
        # retrieve the posted data
        name = request.POST.get('name')
        description = request.POST.get('description')
        expLine = ExpLine(id=explineid)

        # save in the DB
        workflow = AbstractWorkflow(name=name, description=description, expLine=expLine)
        workflow.save()

        # store the response data to send to the html via json by the ajax code
        response_data = {'result': 'Add workflow successful!',
                         'expLineId': explineid,
                         'wkfId': workflow.id,
                         'wkfName': workflow.name
        }

        # send the json to the html
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
            graph = create_graph(eLAct_list, eLActDep_list)

            # derivations_list = Derivation.objects.filter(expLineActivity__expLine_id=explineid)
            # abstractActDep_list = AbstractWorkflowDependency.objects.filter(
            # activity__expLineActivity__expLine__id=explineid)

            cardinality = check_cardinality(graph, eLActDep_list)
            conectivity = check_connectivity(graph)
            # print ('grafo atualizado')
            # store the response data to send to the html via json by the ajax code
            valid = True
            if cardinality or conectivity:
                valid = False

            # createSubGraph(derivations_list, abstractActDep_list)
            form = AbstractWorkflowForm()
        except ExpLineActivity.DoesNotExist:
            raise Http404('ExpLineActivity not exist')

        c = {'eLActDep_list': eLActDep_list,
             'eLAct_list': eLAct_list,
             'expLine': expLine,
             'workflow_list': workflow_list,
             'form': form, 'valid': valid
        }

        return render(request, 'addline/addAbstractWkf.html', c)