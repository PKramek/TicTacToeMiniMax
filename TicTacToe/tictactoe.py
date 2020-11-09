from typing import Tuple, List


class TicTacToe:
    EMPTY = ''
    FIRST = 'O'
    SECOND = 'X'

    # Used to indicate that there was a draw at the end of the game
    FIRST_WON = 'O won'
    SECOND_WON = 'X won'
    DRAW = 'Draw'

    def __init__(self):
        # to allow for different representations of the board
        self.board = [
            [self.EMPTY, self.EMPTY, self.EMPTY],
            [self.EMPTY, self.EMPTY, self.EMPTY],
            [self.EMPTY, self.EMPTY, self.EMPTY]
        ]
        self.winner = None

    def print_board(self):
        for row in self.board:
            print(row)

    def empty_board(self):
        self.board = [
            [self.EMPTY, self.EMPTY, self.EMPTY],
            [self.EMPTY, self.EMPTY, self.EMPTY],
            [self.EMPTY, self.EMPTY, self.EMPTY]
        ]

    def are_any_moves_left(self):
        moves_left = False

        for row in self.board:
            for column in row:
                if column == self.EMPTY:
                    moves_left = True
                    return moves_left

        return moves_left

    def get_all_possible_moves(self) -> List[Tuple[int, int]]:
        possible_moves = []
        for x in range(3):
            for y in range(3):
                if self.board[x][y] == self.EMPTY:
                    possible_moves.append((x, y))

        return possible_moves

    def make_move(self, x: int, y: int, player: str) -> bool:
        move_made = False
        print(self.board[x][y])
        if self.board[x][y] == self.EMPTY:
            self.board[x][y] = player
            move_made = True

        return move_made

    def is_game_over(self):
