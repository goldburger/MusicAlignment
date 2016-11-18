from processing import Graph, SrcNode, OpNode

with Graph('test') as g:
    s = SrcNode('input_file', str)
    o = OpNode('open_file', open, [s], None)

    s.set_value('README.md')
    print(o._value)
