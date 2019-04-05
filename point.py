class Point(object):

    available_id = 0

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.myid = Point.available_id
        Point.available_id += 1

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
