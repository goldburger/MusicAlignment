from processing.exceptions import *

class Graph(object):
    def __init__(self, name):
        self._name = name
        self._nodes = []

    def __enter__(self):
        global global_graph, default_graph
        default_graph = global_graph
        global_graph = self
        return self

    def __exit__(self, type, value, traceback):
        global global_graph, default_graph
        global_graph = default_graph

    def add_node(self, node):
        if type(node) == OpNode:
            self._verify_dependencies(node)
        self._nodes.append(node)

    def _verify_dependencies(self, node):
        for dependency in node._dependencies:
            if dependency not in self._nodes:
                raise MissingDependencyException(
                    'Missing dependency {0} for node {1}'.format(dependency._name, node._name)
                )
            dependency._observers.add(node)

    def __repr__(self):
        return self._name + ": " + str(len(self._nodes)) + " nodes"

default_graph = Graph('default')
global_graph = default_graph

class Node(object):
    def __init__(self, name, value_type=None):
        global global_graph

        self._graph = global_graph      # set the graph to the current global
        self._value = None              # initialize the current value to None
        self._name = name               # initialize our node name
        self._observers = set([])
        self._value_type = value_type

        self._graph.add_node(self)      # insert this node in the graph

    def set_value(self, value):
        if self._value_type and type(value) != self._value_type:
            raise NodeTypeException

        self._value = value
        for observer in self._observers:
            observer.get_value()

class SrcNode(Node):
    def get_value(self):
        return self._value

class OpNode(Node):
    def __init__(self, name, f, dependencies, value_type=None):
        if len(dependencies) == 0:
            raise NoDependencyException

        self._f = f
        self._dependencies = dependencies
        # we need to set dependencies first, so the graph can verify them
        super().__init__(name, value_type)

    def get_value(self):
        self.set_value(self._f(*[v._value for v in self._dependencies]))
