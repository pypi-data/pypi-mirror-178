import argparse
import os.path
import sys

import matplotlib.pyplot as plt
import networkx as nx

from acycling_digraph_problem import parser, Graph


def show_networkx_digraph(g):
    pos = nx.get_node_attributes(g, 'pos')

    edges, colors = zip(*nx.get_edge_attributes(g, 'color').items())
    nx.draw_networkx_nodes(g, pos, node_size=400)
    nx.draw_networkx_labels(g, pos)
    nx.draw_networkx_edges(g, pos, edge_color=colors, arrows=True)
    plt.figure(figsize=(400, 200), dpi=10)
    plt.show()


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def main():
    arg_parser = argparse.ArgumentParser(description="")
    arg_parser.add_argument("file_path", type=str, help="path to input file")
    arg_parser.add_argument('--show', type=str2bool, default=False, help='show graph (default: False)')
    args = arg_parser.parse_args()
    file_path = args.file_path
    show = args.show

    if not os.path.isfile(file_path):
        print("File doesnt exist", file=sys.stderr)
        sys.exit(1)

    with open(file_path, encoding="utf-8") as file:
        source_edges = parser.parse_edges(file)
        graph = Graph()
        graph.add_edges(source_edges)
        star_graphs = graph.get_stars()

        for edge in star_graphs.get_new_edges():
            print(edge)

        edges = star_graphs.get_edges()
        new_edges = star_graphs.get_new_edges()
        g = star_graphs.get_networkx_digraph(edges, new_edges)

        if len(edges) > 1:
            if show:
                show_networkx_digraph(g)
        else:
            print("nothing to do. input file is empty")


if __name__ == "__main__":
    main()
