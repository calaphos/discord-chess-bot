import numpy as np
import itertools


unicodeMappings = {
    b"king_w": "\u2654",
    b"queen_w": "\u2655",
    b"rook_w": "\u2656",
    b"bishop_w": "\u2657",
    b"knight_w": "\u2658",
    b"pawn_w": "\u2659",
    b"king_b": "\u265A",
    b"queen_b": "\u265B",
    b"rook_b": "\u265C",
    b"bishop_b": "\u265D",
    b"knight_b": "\u265E",
    b"pawn_b": "\u265F",
    b'': " "    # empty field
}

movement_mappings = {
}

class chessfield():
    def __init__(self):
        self.field = np.zeros((8, 8), dtype="|S12")

    def init_white(self):
        self.field[:, 1] = "pawn_w"
        self.field[0, 0] = self.field[7, 0] = "rook_w"
        self.field[1, 0] = self.field[6, 0] = "knight_w"
        self.field[2, 0] = self.field[5, 0] = "bishop_w"
        self.field[3, 0] = "queen_w"
        self.field[4, 0] = "king_w"

    def init_black(self):
        field_tmp = np.fliplr(self.field)
        # exchange _w for _b:
        field_tmp = np.vectorize(lambda s: s.replace(b"_w", b"_b"))(field_tmp)
        self.field[:,6:] = field_tmp[:,-2:]


    def move(self, origin, destination):
        """move the specified piece to a position"""
        piece = self.field[origin]

        if not self.check_valid_move(origin, destination):
            raise InvalidCoordinatesException

        self.field[origin] = b""
        self.field[destination] = piece
        return piece


    def board_as_unicode(self):
        return np.vectorize(lambda s: unicodeMappings[s])(self.field)

    def check_valid_move(self, origin, destination):
        #TODO
        piece = self.field[origin]


        return True

    @staticmethod
    def piece_as_unicode(piece):
        return unicodeMappings[piece]

    def valid_king_movement(self, origin, destination):
        valid_positions = [origin - d for d in itertools.product(range(-1,2), range(-1,2))]
        # not moving is not allowed

    def valid_rook_movement(self, origin, destination):
        pass

class InvalidCoordinatesException(Exception):
    pass

if __name__ == '__main__':
    f = chessfield()
    f.init_white()
    f.init_black()
    print(f.field)
    print(f.board_as_unicode())
