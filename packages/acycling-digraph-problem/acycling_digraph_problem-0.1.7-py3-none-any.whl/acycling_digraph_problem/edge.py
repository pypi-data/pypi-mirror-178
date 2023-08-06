from dataclasses import dataclass


@dataclass
class Edge:
    vertex: str
    vertex_to: str
    color: str = 'red'

    def __repr__(self):
        return f"{self.vertex} -> {self.vertex_to}"
