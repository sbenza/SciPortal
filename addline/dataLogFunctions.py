from pyDatalog.pyDatalog import *
from addline.models import *
from addline.expLineDataLog import *

#
# pyDatalog.create_atoms('X', 'Y')
#
# # pyDatalog.clear()
# # @pyDatalog.predicate()
# def teste():
#     pyDatalog.clear()
#
#     @pyDatalog.predicate()
#     def _():
#         X, Y = pyDatalog.variables(2)
#         #
#         # Act1= ExpLineActivityDataLog(ExpLineActivity.objects.get(id=1))
#         # Act2= ExpLineActivityDataLog(ExpLineActivity.objects.get(id=2))
#         act_list = []
#         for i in range(1, 3):
#             act_list.append(ExpLineActivityDataLog(ExpLineActivity.objects.get(id=i)))
#         print(act_list[0].expLine.id)
#         # (ExpLineActivityDataLog.expLine[X]==Act1.expLine)
#         var = (ExpLineActivityDataLog.expLine[X] == Y)
#         print(X, Y)
#         return X
#
#     t = []
#     for i in _().data:
#         t.append(i)
#     return t


# @pyDatalog.program()
# def teste():
# Act1= ExpLineActivityDataLog(ExpLineActivity.objects.get(id=1))
# Act2= ExpLineActivityDataLog(ExpLineActivity.objects.get(id=2))
# Act3= ExpLineActivityDataLog(ExpLineActivity.objects.get(id=3))
#
#     pyDatalog.create_terms('has_car, X')
#     # + has_car(Act1)
#     # return (has_car(X))
#     assert_fact('has_car',Act1)
#     a =  ask('has_car(X)')
#     return a
def check_cardinality(graph,dependencies):
    pyDatalog.clear()
    print (dependencies)
    @pyDatalog.predicate()
    def _():
        #todo
        in_cardinality_dict={}
        invalid_in_text=''

        for in_degree_tuple in graph.iterindegree():
            ela=ExpLineActivity.objects.get(id=int(in_degree_tuple[0]))
            #saves the object and its cardinality
            if in_degree_tuple[1] >= 2:
                if ela.operation.upper() != 'QUERY':

                    in_cardinality_dict[ela.id]=(ela, ela.operation, in_degree_tuple[1])

        items= in_cardinality_dict.items()
        new_dict={}
        for k,v in items:
            dep=dependencies.filter(dependentELActivity=v[0])
            for i in dep:
                if not i.optional:
                    new_dict[k]=v
                    break


        for k,v in new_dict.items():
            invalid_in_text+= ('The Activity '+ (v[0].name).upper() + ' has ' + str(v[2]) +
                                       ' dependencies. (Should be only 1 or less). <br/>' )

        # dep=dependencies.objects.filter(depexplineactid=ela.id)
        # for i in dep:
        #     if i.explineactid

        return invalid_in_text
        # print (in_cardinality_dict, invalid_in_text)
        # X=pyDatalog.create_atoms()
        # pyDatalog.create_terms('in, out, X, Y')
        # pyDatalog.assert_fact('in','MAP',1)
        # pyDatalog.assert_fact('in','FILTER',1)
        # pyDatalog.assert_fact('in','SPLITMAP',1)
        # pyDatalog.assert_fact('in','REDUCE',1)
        # pyDatalog.assert_fact('in','MRQUERY',X)
    return _()


def check_connectivity(graph):
    pyDatalog.clear()

    @pyDatalog.predicate()
    def _():
        #creating terms in facts database
        pyDatalog.create_terms('link, X, Y')

        edges = graph.edges()
        for i in edges:
            pyDatalog.assert_fact('link', i[0], i[1])
            pyDatalog.assert_fact('link', i[1], i[0])
            load('can_reach(X,Y) <= can_reach(X,Z) & link(Z,Y) & (X!=Y)')
            load('can_reach(X,Y) <= link(X,Y)')

        #checking links
        question = '(can_reach("' + i[0] + '",Y))'
        a = (ask(question))
        # t=[i[0]]
        nodes = graph.nodes()
        nodes.remove(i[0])
        for i in a.answers:
            # t.append(i[0])
            nodes.remove(i[0])

        #get nodes names to show in message
        nodes_name = ''
        for i in nodes:
            nodes_name += (str(i.attr['label'])) + ', '

        #return only if not connected
        if not nodes:
            #todo
            # print('Graph is connected')  #console text
            pass
        else:
            # print('Graph is not connected, nodes separated from graph: ', nodes)  #console text
            return 'Graph is not connected, nodes separated from graph: ', nodes_name

    return _()
