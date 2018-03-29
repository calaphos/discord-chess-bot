from coordinates import Coordinate as C, Direction as D
from itertools import product
standard_positions = {C(2, 7): b'bishop_b', C(4, 7): b'king_b', C(2, 6): b'pawn_b', C(3, 6): b'pawn_b', C(6, 6): b'pawn_b',
                      C(3, 0): b'queen_w', C(7, 1): b'pawn_w', C(6, 0): b'knight_w', C(2, 1): b'pawn_w', C(7, 7): b'rook_b',
                      C(5, 6): b'pawn_b', C(0, 0): b'rook_w', C(1, 6): b'pawn_b', C(0, 7): b'rook_b', C(5, 1): b'pawn_w',
                      C(3, 7): b'queen_b', C(1, 0): b'knight_w', C(4, 0): b'king_w', C(0, 1): b'pawn_w', C(7, 0): b'rook_w',
                      C(6, 7): b'knight_b', C(4, 6): b'pawn_b', C(0, 6): b'pawn_b', C(6, 1): b'pawn_w', C(3, 1): b'pawn_w',
                      C(2, 0): b'bishop_w', C(7, 6): b'pawn_b', C(5, 0): b'bishop_w', C(1, 7): b'knight_b',
                      C(5, 7): b'bishop_b', C(4, 1): b'pawn_w', C(1, 1): b'pawn_w'}

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
}


class ChessBoard(object):


    def __init__(self):
        """inits a new chess board with standard piece positions.
        the board is saved as a dict with coordindats for keys"""
        self.board = standard_positions

    def show_board(self):
        board = ""
        for x in range(8):
            for y in range(8):
                if C(x,y) in self.board:
                    board += unicodeMappings[self.board[C(x,y)]]
                else:
                    board += " "
            board += "\n"

        return board

    def move(self, origin: C, destination: C) -> str:
        """moves a piece form origin to destination. Does validiy checks. Returns a nicely formatted string message"""
        if not self.is_valid_move(origin, destination):
            raise InvalidMoveException

        piece = self.board[origin]
        return "Moved {} fom {} to {}".format(unicodeMappings[piece], origin.as_chess_notation(), destination.as_chess_notation())


    def is_occupied(self, pos:C, colour):
        if self.board[pos][-2:] == colour:
            return True
        else:
            return False


    def is_valid_move(self, origin, destination):
        if origin not in self.board: return False
        piece = self.board[origin]
        return piece_movement_mappings[piece](self, origin, destination)


    def valid_moves_in_direction(self, orig: C, d_vec:D)->[C]:
        """returns how far pieces can move into a direction, before encountering another piece"""
        colour = self.board[orig][-2:]
        valid = []
        for d in range(-7,8):
            try:
                pos = orig + d_vec * d
            except ValueError:
                # out of board.
                break

            if pos not in self.board:
                # empty position, move along
                valid.append(pos)
            elif self.board[pos][-2:] == colour:
                # own piece, cant move further
                break
            else:
                # enemy piece
                valid.append(pos)
                break


    def valid_king_move(self, origin, destination):
        movemets = [C(*i) for i in product(range(-1,2), range(-1,2))]
        movemets.remove(C(0,0))  # cant stay on the same position
        valid_positions = [origin + move for move in movemets]
        colour = self.board[origin][-2:]
        if destination in valid_positions and not self.is_occupied(destination, colour):
            return True
        else: return False

    def valid_queen_movement(self, origin, destination):
        valid_directions = [i for i in product(range(-1,2), range(-1,2))]
        valid_directions.remove((0,0))

        valid_pos = []
        for direction in valid_directions:
            valid_pos.append(self.valid_moves_in_direction(origin, D(*direction)))

        if destination in valid_pos: return True
        else: return False

    def valid_rook_movement(self, origin, destination):
        valid_directions = [(1,0), (0,1), (-1,0), (0,-1)]
        valid_pos = []
        for direction in valid_directions:
            valid_pos.append(self.valid_moves_in_direction(origin, D(*direction)))

        if destination in valid_pos: return True
        else: return False

    def valid_bishop_movement(self, origin, destination):
        valid_directions = [(1,1), (-1,1), (-1,-1), (1,-1)]
        valid_pos = []
        for direction in valid_directions:
            valid_pos.append(self.valid_moves_in_direction(origin, D(*direction)))

        if destination in valid_pos: return True
        else: return False

    def valid_knight_movement(self, origin, destination):
        relative = [(2,-1), (2,1), (1,-2), (1,2), (-2,-1), (-2,1), (-1,2), (-1,-2)]
        absolut = []
        for e in relative:
            try:
                absolut.append(origin + e)
            except ValueError:
                pass

        for pos in absolut:
            if pos not in self.board:
                return True
            if self.board[pos][-2:] != self.board[origin][-2:]:
                return True
            else:
                return False

    def valid_pawn_movement_b(self, origin, destination):
        pass






piece_movement_mappings = {
    b"king_w": ChessBoard.valid_king_move,
    b"kind_b":ChessBoard.valid_king_move,
    b"quen_w":ChessBoard.valid_queen_movement,
    b"queen_b":ChessBoard.valid_queen_movement,
    b"rook_w": ChessBoard.valid_rook_movement,
    b"rook_b": ChessBoard.valid_rook_movement,
    b"bishop_w": ChessBoard.valid_bishop_movement,
    b"bishop_b": ChessBoard.valid_bishop_movement,
    b"knight_w": ChessBoard.valid_knight_movement,
    b"knight_b": ChessBoard.valid_knight_movement,

}


class InvalidMoveException(Exception):
    pass
