from io import StringIO

import matplotlib.pyplot as plt
import networkx as nx

import parser
from graph import Graph


def show_networkx_digraph(g):
    pos = nx.get_node_attributes(g, 'pos')

    edges, colors = zip(*nx.get_edge_attributes(g, 'color').items())
    nx.draw_networkx_nodes(g, pos, node_size=400)
    nx.draw_networkx_labels(g, pos)
    nx.draw_networkx_edges(g, pos, edge_color=colors, arrows=True)
    plt.figure(figsize=(400, 200), dpi=10)
    plt.show()


graph_input = """r1 -> p1
r1 -> p2
r1 -> p3
r2 -> p4
r2 -> p5
r2 -> p6
p7 -> r3
p8 -> r3
p9 -> r3
p10 -> r4
p11 -> r4
p12 -> r4
p13 -> r5
p14 -> r5
p15 -> r5"""

source_edges = parser.parse_edges(StringIO(graph_input))
graph = Graph()
graph.add_edges(source_edges)
star_graphs = graph.get_stars()

for edge in star_graphs.get_new_edges():
    print(edge)

g = star_graphs.get_networkx_digraph(star_graphs.get_edges(), star_graphs.get_new_edges())

show_networkx_digraph(g)
