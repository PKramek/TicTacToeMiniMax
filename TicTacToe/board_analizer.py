from typing import List, Tuple


class BoardAnalizer:

    def __init__(self, tic_tac_toe_game: 'TicTacToe'):
        self.game = tic_tac_toe_game

    def get_all_possible_moves(self, board: List[List['str']]) -> List[Tuple[int, int]]:
        possible_moves = []
        for x in range(3):
            for y in range(3):
                if board[x][y] == self.game.EMPTY:
                    possible_moves.append((x, y))

        return possible_moves

    def get_board_after_move(self, board: List[List['str']], x: int, y: int, player: str):
        pass