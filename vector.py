from point import *
from math import sqrt
import tkinter as tk


class Vector(object):

    available_id = 0

    def __init__(self, p=Point()):
        self.x = p.x
        self.y = p.y
        self.myid = Vector.available_id
        Vector.available_id += 1

    def __add__(self, other):
        return Vector(Point(self.x + other.x, self.y + other.y))

    def __sub__(self, other):
        return Vector(Point(self.x - other.x, self.y - other.y))

    def __matmul__(self, other):
        """Pseudovector multiplication"""
        return self.x * other.y - self.y * other.x

    def __mul__(self, other):
        """Scalar multiplication"""
        return self.x * other.x + self.y * other.y

    def __abs__(self):
        return sqrt(self * self)

    def __str__(self):
        return "{" + str(self.x) + ", " + str(self.y) + "}"
