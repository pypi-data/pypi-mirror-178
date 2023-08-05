from edge import Edge


def parse_edges(io_stream, sep='->') -> list[Edge]:
    edges = []

    for line in io_stream:
        vertex, vertex_to = list(map(lambda x: x.strip(), line.split(sep)))
        edges.append(Edge(vertex, vertex_to))

    return edges
