from figures import *


def is_convex(pg: Polygon):
    sgn = pg.edges[-1] @ pg.edges[0]
    for i in range(0, len(pg.edges) - 1):
        if sgn == 0:
            sgn = pg.edges[i] @ pg.edges[i + 1]
        elif sgn * (pg.edges[i] @ pg.edges[i + 1]) < 0:
            return False
    return True


def get_perimeter(f: Polygon):
    res = 0
    for e in f.edges:
        res += abs(e)
    return res


def get_square(f: Polygon):
    res = 0
    for i in range(0, len(f.vertexes) - 1):
        res += (f.vertexes[i - 1].x - f.vertexes[i].x) * (f.vertexes[i - 1].y + f.vertexes[i].y)
    return abs(res) / 2
