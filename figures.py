from point import *
from vector import *


class Figure(object):
    pass


class Polygon(Figure):
    vertexes = []
    edges = []

    def __init__(self, vertexes: []):
        self.vertexes = vertexes
        for i in range(0, len(self.vertexes) - 1):
            self.edges.append(Vector(vertexes[i + 1] - vertexes[i]))
        self.edges.append(Vector(vertexes[0] - vertexes[len(self.vertexes) - 1]))
