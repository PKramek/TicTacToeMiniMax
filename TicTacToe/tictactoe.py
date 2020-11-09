import copy
from typing import Tuple, List


class TicTacToe:
    EMPTY = ''
    FIRST = 'O'
    SECOND = 'X'

    # Used to indicate that there was a draw at the end of the game
    FIRST_WON = 'O won'
    SECOND_WON = 'X won'
    TIE = 'Tie'

    def __init__(self):
        # to allow for different representations of the board
        self.board = None
        self.winner = None

        self.reset_game()

    def reset_game(self):
        self.board = [
            [self.EMPTY, self.EMPTY, self.EMPTY],
            [self.EMPTY, self.EMPTY, self.EMPTY],
            [self.EMPTY, self.EMPTY, self.EMPTY]
        ]
        self.winner = None

    @staticmethod
    def get_all_possible_moves_for_board(board: List[List['str']]) -> List[Tuple[int, int]]:

        possible_moves = []
        for x in range(3):
            for y in range(3):
                if board[x][y] == TicTacToe.EMPTY:
                    possible_moves.append((x, y))

        return possible_moves

    @staticmethod
    def get_board_state_after_move_for_board(x: int, y: int, player: str,
                                             board: List[List['str']]
                                             ) -> List[List['str']]:
        board_copy = copy.deepcopy(board)
        if board_copy[x][y] == TicTacToe.EMPTY:
            board_copy[x][y] = player
        else:
            raise ValueError('Position x={}, y={} is not empty'.format(x, y))

        return board_copy

    @staticmethod
    def get_winner_for_board(board: List[List['str']]):
        # horizontal
        for i in range(len(board)):
            if board[i][0] != TicTacToe.EMPTY and board[i][0] == board[i][1] == board[i][2]:
                return board[i][0]

        # vertical
        for i in range(len(board)):
            if board[0][i] != TicTacToe.EMPTY and board[0][i] == board[1][i] == board[2][i]:
                return board[0][i]

        # first diagonal
        if board[0][0] != TicTacToe.EMPTY and board[0][0] == board[1][1] == board[2][2]:
            return board[0][0]

        # second diagonal
        elif board[0][2] != TicTacToe.EMPTY and board[0][2] == board[1][1] == board[2][0]:
            return board[0][2]

        elif not TicTacToe.any_moves_left_for_board(board):
            return TicTacToe.TIE

        return None

    @staticmethod
    def any_moves_left_for_board(board: List[List['str']]) -> bool:
        for row in board:
            for column in row:
                if column == TicTacToe.EMPTY:
                    return True

        return False

    def is_over(self):
        winner = self.get_winner_for_board(self.board)
        if winner is not None:
            self.winner = winner

        return winner is not None

    def get_all_possible_moves(self):
        return self.get_all_possible_moves_for_board(self.board)

    def make_move(self, x: int, y: int, player: str):
        try:
            board = self.get_board_state_after_move_for_board(x, y, player, self.board)
        except ValueError as e:
            raise e
        else:
            self.board = board
        # TODO refactor this try-catch code

    def print_board(self):
        for row in self.board:
            print(row)
