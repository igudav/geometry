from figures import *


def is_convex(pg: Polygon):
    sgn = pg.edges[-1] @ pg.edges[0]
    for i in range(0, len(pg.edges) - 1):
        if sgn == 0:
            sgn = pg.edges[i] @ pg.edges[i + 1]
        elif sgn * (pg.edges[i] @ pg.edges[i + 1]) < 0:
            return False
    return True
