from typing import Tuple, List


class TicTacToe:
    EMPTY = ''
    FIRST = 'O'
    SECOND = 'X'
    TIE = 'Tie'

    def __init__(self):
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
    def get_winner_for_board(board: List[List['str']]):
        """

        :param board:
        :type board:
        :return: Return None if there is no winner or one of the constants: [TicTacToe.FIRST,
                                                                            TicTacToe.SECOND,
                                                                            TicTacToe.TIE]
        :rtype: str
        """
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

        # If no moves left that means that there is a tie
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

    @staticmethod
    def get_other_player(current_player):
        lookup = {
            TicTacToe.FIRST: TicTacToe.SECOND,
            TicTacToe.SECOND: TicTacToe.FIRST
        }
        return lookup[current_player]

    def make_move(self, x: int, y: int, player: str):
        if self.board[x][y] == TicTacToe.EMPTY:
            self.board[x][y] = player
        else:
            raise ValueError('Position x={}, y={} is not empty'.format(x, y))

        return self.board

    def undo_move(self, x: int, y: int, player: str):
        if self.board[x][y] == player:
            self.board[x][y] = TicTacToe.EMPTY
        else:
            raise ValueError('Position x={}, y={} is empty'.format(x, y))

        return self.board

    def is_over(self):
        winner = self.get_winner_for_board(self.board)
        if winner is not None:
            self.winner = winner

        return winner is not None

    def get_all_possible_moves(self):
        return self.get_all_possible_moves_for_board(self.board)

    def print_board(self):
        print('##' * 20)
        for row in self.board:
            print(row)
        print('##' * 20)
