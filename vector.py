from point import *
from math import sqrt


class Vector(object):

    def __init__(self, p=Point()):
        self.x = p.x
        self.y = p.y

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
