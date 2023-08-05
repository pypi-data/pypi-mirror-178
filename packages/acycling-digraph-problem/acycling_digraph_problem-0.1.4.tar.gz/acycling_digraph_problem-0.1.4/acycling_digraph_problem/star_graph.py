from dataclasses import dataclass
from enum import Enum

import networkx as nx

from acycling_digraph_problem.edge import Edge
from acycling_digraph_problem.utils import pairwise


class StarGraphType(Enum):
    first_cluster = "first_cluster"
    second_cluster = "second_cluster"


@dataclass
class StarGraph:
    type: StarGraphType
    vertex: str
    adj_vertex: list[str]

    def is_first_cluster(self) -> bool:
        return self.type == StarGraphType.first_cluster

    def is_second_cluster(self) -> bool:
        return self.type == StarGraphType.second_cluster

    def type_is(self, type_):
        return self.type == type_


class StarGraphs:
    graphs: list[StarGraph]
    first_cluster_count: int
    second_cluster_count: int

    def __init__(self):
        self.graphs = []
        self.first_cluster_count = 0
        self.second_cluster_count = 0

    def add_graph(self, graph) -> None:
        self.graphs.append(graph)
        if graph.is_first_cluster():
            self.first_cluster_count += 1
        else:
            self.second_cluster_count += 1

    def get_edges(self) -> list[Edge]:
        result = []
        for graph in self.graphs:
            for adj_v in graph.adj_vertex:
                if graph.is_first_cluster():
                    result.append(Edge(graph.vertex, adj_v))
                else:
                    result.append(Edge(adj_v, graph.vertex))
        return result

    def get_clusters_vertexes(self) -> tuple[list[str], list[str]]:
        first_cluster_vertex, second_cluster_vertex = [], []
        for i, structured_graph in enumerate(self.graphs):
            if structured_graph.type == StarGraphType.first_cluster:
                first_cluster_vertex += structured_graph.adj_vertex
            else:
                if i == len(self.graphs) - 1:
                    second_cluster_vertex += structured_graph.adj_vertex
                else:
                    second_cluster_vertex += structured_graph.adj_vertex[:-1]
        return first_cluster_vertex, second_cluster_vertex

    def get_new_edges(self) -> list[Edge]:
        result = []
        if self.first_cluster_count > 0 and self.second_cluster_count == 0 or \
                self.first_cluster_count == 0 and self.second_cluster_count:

            for g1, g2 in pairwise(self.graphs, True):
                if self.first_cluster_count > 0:
                    result.append(Edge(g1.adj_vertex[-1], g2.vertex))
                else:
                    result.append(Edge(g1.vertex, g2.adj_vertex[0]))

            for g in self.graphs:
                for v1, v2 in pairwise(g.adj_vertex, False):
                    result.append(Edge(v1, v2))
        else:
            for g1, g2 in pairwise(self.graphs, False):
                if g1.type == StarGraphType.first_cluster:
                    if g2.type == StarGraphType.first_cluster:
                        result.append(Edge(g2.adj_vertex[0], g1.vertex))
                    else:
                        result.append(Edge(g2.vertex, g1.vertex))
                else:
                    if g2.type == StarGraphType.first_cluster:
                        result.append(Edge(g2.vertex, g1.vertex))
                    else:
                        result.append(Edge(g2.vertex, g1.adj_vertex[-1]))

            first_cluster_vertex, second_cluster_vertex = self.get_clusters_vertexes()

            i = 0
            for v1, v2 in zip(first_cluster_vertex, second_cluster_vertex):
                result.append(Edge(v1, v2))
                i += 1

            j = i - 1
            while i < len(first_cluster_vertex):
                result.append(Edge(first_cluster_vertex[i], second_cluster_vertex[j]))
                i += 1
            while i < len(second_cluster_vertex):
                result.append(Edge(first_cluster_vertex[j], second_cluster_vertex[i]))
                i += 1

        return result

    def get_edges_for_strongly_connected_one(self) -> list[Edge]:
        pass

    def get_networkx_digraph(self, edges, new_edges) -> nx.DiGraph:
        g = nx.DiGraph()

        # add nodes and calc positions
        first_part_pos_x = 20
        second_part_pos_x = 18
        padding = 10000
        global_padding = padding
        for structured_graph in self.graphs:

            first_part_pos_x_local = second_part_pos_x
            second_part_pos_x_local = first_part_pos_x

            if structured_graph.is_first_cluster():
                first_part_pos_x_local = first_part_pos_x
                second_part_pos_x_local = second_part_pos_x

            vertex_len = len(structured_graph.adj_vertex)
            global_padding += padding
            g.add_node(structured_graph.vertex,
                       pos=(global_padding + ((2 * vertex_len) * padding) / 2, first_part_pos_x_local))

            for i, adj_vertex_ in enumerate(structured_graph.adj_vertex):
                global_padding += padding
                g.add_node(adj_vertex_, pos=(global_padding + padding, second_part_pos_x_local))

        # add edges
        for edge in edges:
            g.add_edge(edge.vertex, edge.vertex_to, color='blue')

        # add new edges
        for edge in new_edges:
            g.add_edge(edge.vertex, edge.vertex_to, color='red')

        return g
