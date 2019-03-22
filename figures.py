from point import *
from vector import *


class Figure(object):

    available_id = 0

    def __init__(self):
        self.myid = Figure.available_id
        Figure.available_id += 1


class Polygon(Figure):

    def __init__(self, vertexes=None):
        super().__init__()
        self.edges = []
        self.vertexes = []
        if vertexes is not None:
            self.vertexes = vertexes
            for i in range(0, len(self.vertexes) - 1):
                self.edges.append(Vector(vertexes[i + 1] - vertexes[i]))
            self.edges.append(Vector(vertexes[0] - vertexes[len(self.vertexes) - 1]))

    def add_vertex(self, p: Point):
        self.vertexes.append(p)
        ln = len(self.vertexes)
        if ln == 2:
            self.edges.append(Vector(self.vertexes[-1] - self.vertexes[-2]))
            self.edges.append(Vector(self.vertexes[0] - self.vertexes[-1]))
        elif ln > 2:
            self.edges.pop()
            self.edges.append(Vector(self.vertexes[-1] - self.vertexes[-2]))
            self.edges.append(Vector(self.vertexes[0] - self.vertexes[-1]))

    def pop_vertex(self):
        self.vertexes.pop()
        self.edges.pop()
        self.edges.pop()
        self.edges.append(Vector(self.vertexes[0] - self.vertexes[-1]))
