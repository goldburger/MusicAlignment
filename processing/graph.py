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
        print(type(node))
        self._nodes.append(node)

    def __repr__(self):
        return self._name + ": " + str(len(self._source_nodes)) + " source nodes"

default_graph = Graph('default')
global_graph = default_graph

class GraphTypeException(Exception):
    pass

class Node(object):
    def __init__(self, name, value_type):
        global global_graph

        self._graph = global_graph      # set the graph to the current global
        self._value = None              # initialize the current value to None
        self._name = name               # initialize our node name
        self._value_type = value_type   # the Maybe type of our value

        self._graph.add_node(self)

    def set_value(self, value):
        if type(value) == self._value_type:
            self._value = value
        else:
            raise GraphTypeException

class SrcNode(Node):
    def get_value(self):
        return self._value

class OpNode(Node):
    def __init__(self, ):
        super().__init__()
        # in this case, the name defaults to 'op_{0}'
        self._name = name
        if not name:
            self._name = 'op_{0}'.format(len(self._graph._op_nodes))
        # assure our op node actually has dependencies
        assert(len(deps) > 0)

        self._f = f
        self._graph._add_op(self)

    def run(self):
        pass
