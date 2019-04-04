from point import *
from vector import *
import tkinter as tk


class Figure(object):

    available_id = 0

    def __init__(self, canvas: tk.Canvas = None):
        self.myid = Figure.available_id
        Figure.available_id += 1
        self.cv = canvas
        self.line_ordinary_style = dict(width=2, fill='black')
        self.point_ordinary_style = dict(fill="yellow", outline="black")
        self.line_selected_style = dict(width=4, fill="lightblue")
        self.selected = False
        self.destroyed = False


class Polygon(Figure):

    def __init__(self, canvas: tk.Canvas = None, vertexes=None):
        super().__init__(canvas)
        self.edges = []
        self.vertexes = []
        self.lines = []
        self.points = []
        if vertexes is not None:
            self.vertexes = vertexes
            for i in range(0, len(self.vertexes) - 1):
                self.edges.append(Vector(vertexes[i + 1] - vertexes[i]))
                if self.cv is not None and len(vertexes) > 1:
                    self.lines.append(self.cv.create_line(self.vertexes[i - 1].x, self.vertexes[i - 1].y,
                                                          self.vertexes[i].x, self.vertexes[i].y,
                                                          self.line_ordinary_style))
            self.edges.append(Vector(vertexes[0] - vertexes[len(self.vertexes) - 1]))

    def add_vertex(self, p: Point):
        self.vertexes.append(p)
        ln = len(self.vertexes)
        if self.cv is not None:
            self.points.append(self.cv.create_oval(self.vertexes[-1].x - 3,
                                                   self.vertexes[-1].y - 3,
                                                   self.vertexes[-1].x + 3,
                                                   self.vertexes[-1].y + 3,
                                                   self.point_ordinary_style))
        if ln == 2:
            self.edges.append(Vector(self.vertexes[1] - self.vertexes[0]))
            self.edges.append(Vector(self.vertexes[0] - self.vertexes[1]))
            if self.cv is not None:
                self.lines.append(self.cv.create_line(self.vertexes[1].x, self.vertexes[1].y,
                                                      self.vertexes[0].x, self.vertexes[0].y,
                                                      self.line_ordinary_style))
        elif ln > 2:
            self.edges.pop()
            self.edges.append(Vector(self.vertexes[-1] - self.vertexes[-2]))
            self.edges.append(Vector(self.vertexes[0] - self.vertexes[-1]))
            if self.cv is not None:
                self.lines.append(self.cv.create_line(self.vertexes[-1].x, self.vertexes[-1].y,
                                                      self.vertexes[-2].x, self.vertexes[-2].y,
                                                      self.line_ordinary_style))

    def finish_adding_verts(self):
        self.lines.append(self.cv.create_line(self.vertexes[-1].x, self.vertexes[-1].y,
                                              self.vertexes[0].x, self.vertexes[0].y,
                                              self.line_ordinary_style))

    def pop_vertex(self):
        self.vertexes.pop()
        self.cv.delete(self.points.pop())
        self.cv.delete(self.lines.pop())
        self.edges.pop()
        self.edges.pop()
        self.edges.append(Vector(self.vertexes[0] - self.vertexes[-1]))

    def select(self):
        if not self.selected:
            for a in self.lines:
                self.cv.itemconfig(a, self.line_selected_style)
                self.selected = True
            return 1
        else:
            for a in self.lines:
                self.cv.itemconfig(a, self.line_ordinary_style)
                self.selected = False
            return -1

    def destroy(self):
        for a in self.lines:
            self.cv.delete(a)
        for b in self.points:
            self.cv.delete(b)
        self.destroyed = True

    # TODO разобраться с ошибкой при закрытии программы
    def __del__(self):
        for a in self.lines:
            self.cv.delete(a)
        for b in self.points:
            self.cv.delete(b)
