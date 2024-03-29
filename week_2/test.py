from graphviz import Digraph

dot = Digraph(comment='The Round Table')
dot.node('A1', 'King Arthur')
dot.node('B', 'Sir Bedevere the Wise')
dot.node('L', 'Sir Lancelot the Brave')
dot.edge('A1', 'B')
dot.edge('B', 'L', constraint='false')
print(dot.source)
dot.render('test-output/round-table.gv', view=True)
