from processing import Graph, SrcNode

with Graph('test') as g:
    s = SrcNode('filename', str)
    s.set_value('test')
    print(s.get_value())
