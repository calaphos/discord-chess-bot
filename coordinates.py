

class C():

    """This is a class for handling chess coordinates. It does bounds checking, defines movement operations and
    is used to translate between the internal (0,0) based coordintes system to the common (a,1) based chess system"""

    def __init__(self, *args :int):
        self.x, self.y = args

        if self.x not in range(8) or self.y not in range(8):
            raise ValueError()

    def __add__(self, other):
        x, y = other
        return self.x + x, self.y + y

    def __sub__(self, other):
        x, y = other
        return self.x - x, self.y - y

    def as_chess_notation(self):
        return chr(self.x + 97), self.y + 1

