from point import *
from vector import *


class Segment(object):

    def __init__(self, p1: Point = Point(0, 0), p2: Point = Point(0, 0)):
        self.a = p1
        self.b = p2
        self.vec = Vector(self.b - self.a)


def check_intersect(s1: Segment, s2: Segment):
    x1min = min(s1.a.x, s1.b.x)
    x2min = min(s2.a.x, s2.b.x)
    y1min = min(s1.a.y, s1.b.y)
    y2min = min(s2.a.y, s2.b.y)
    x1max = max(s1.a.x, s1.b.x)
    x2max = max(s2.a.x, s2.b.x)
    y1max = max(s1.a.y, s1.b.y)
    y2max = max(s2.a.y, s2.b.y)
    if max(x1min, x2min) > min(x1max, x2max) or max(y1min, y2min) > min(y1max, y2max):
        return False
    if (Vector(s1.b - s2.a) @ Vector(s2.b - s2.a)) * (Vector(s1.a - s2.a) @ Vector(s2.b - s2.a)) > 0:
        return False
    if (Vector(s2.b - s1.a) @ Vector(s1.b - s1.a)) * (Vector(s2.a - s1.a) @ Vector(s1.b - s1.a)) > 0:
        return False
    return True
