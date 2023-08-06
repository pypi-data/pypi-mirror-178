from acycling_digraph_problem.star_graph import StarGraphs, StarGraph, StarGraphType


class Graph:
    g: dict[str, set[str]]

    def __init__(self):
        self.g = dict()

    def add_edge(self, edge) -> None:
        if edge.vertex in self.g:
            self.g[edge.vertex].add(edge.vertex_to)
        else:
            self.g[edge.vertex] = {edge.vertex_to}

    def add_edges(self, edges) -> None:
        for edge in edges:
            self.add_edge(edge)

    def _dfs(self, vertex, used, component_number, components) -> None:
        used[vertex] = True
        components[component_number].append(vertex)

        to_set = set(self.g.get(vertex, []))

        new_values_in_to_set = set()
        for to in to_set:
            for v_, adj_ in self.g.items():
                if to in adj_:
                    new_values_in_to_set.add(v_)

        to_set.update(new_values_in_to_set)

        for to in to_set:
            if not used.get(to, False) and to != vertex:
                self._dfs(to, used, component_number, components)

    def get_components(self) -> dict[int, list[str]]:
        component_number = 1
        components = dict()
        used = dict()

        for v in self.g.keys():
            if not used.get(v, False):
                components[component_number] = []
                self._dfs(v, used, component_number, components)
                component_number += 1

        return components

    def get_stars(self) -> StarGraphs:
        """
        method work correct only if graph contain only stars of first and second clusters
        :return:
        """
        star_graphs = StarGraphs()
        components = self.get_components()

        for component, vertexes in components.items():

            # if first cluster
            root = vertexes[0]  # if item exist then zero index exist
            for vertex in vertexes:
                if vertex in self.g and len(self.g[root]) < len(self.g[vertex]):
                    root = vertex

            if len(self.g[root]) == len(vertexes) - 1:
                star_graphs.add_graph(
                    StarGraph(StarGraphType.first_cluster, root, [vertex for vertex in vertexes if vertex != root]
                              )
                )
                continue

            # else second cluster
            for vertex in vertexes:
                if vertex not in self.g or len(self.g[vertex]) == 0:
                    root = vertex

            star_graphs.add_graph(
                StarGraph(StarGraphType.second_cluster, root, [vertex for vertex in vertexes if vertex != root])
            )

        return star_graphs
