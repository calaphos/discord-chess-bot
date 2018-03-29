

class Coordinate():

    """This is a class for handling chess coordinates. It does bounds checking, defines movement operations and
    is used to translate between the internal (0,0) based coordintes system to the common (a,1) based chess system"""

    def __init__(self, *args :int):
        self.x, self.y = args

        if self.x not in range(8) or self.y not in range(8):
            raise ValueError()

    def __add__(self, other):
        return C(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return C(self.x - other.x, self.y - other.y)

    def __mul__(self, other:int):
        return C(self.x * other, self.y * other)

    def __getattr__(self, item):
        if item == 0: return self.x
        elif item==1: return self.y
        else: raise ValueError()

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def as_chess_notation(self):
        return chr(self.x + 97), self.y + 1

class Direction():
    """like Coordinates, without bounds checking"""
    def __init__(self, *args :int):
        self.x, self.y = args

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coordinate(self.x - other.x, self.y - other.y)

    def __mul__(self, other:int):
        return Coordinate(self.x * other, self.y * other)
