from abc import ABC, abstractmethod
from random import choice as random_choice
from typing import Tuple

from TicTacToe.tictactoe import TicTacToe


class Player(ABC):
    def __init__(self, game: TicTacToe, symbol: str):
        self.game = game
        self.symbol = symbol

    @abstractmethod
    def chose_move(self) -> Tuple[int, int]:
        pass


class RandomPlayer(Player):

    def chose_move(self) -> Tuple[int, int]:
        possible_moves = self.game.get_all_possible_moves()
        move = random_choice(possible_moves)

        return move


class MiniMaxPlayer(Player):
    maximizing_lookup = {TicTacToe.FIRST: True,
                         TicTacToe.SECOND: False}

    def __init__(self, game: TicTacToe, symbol: str, max_depth: int):
        super().__init__(game, symbol)
        self.max_depth = max_depth
        self.is_maximizing = MiniMaxPlayer.maximizing_lookup[self.symbol]

    def chose_move(self) -> Tuple[int, int]:
        possible_moves = self.game.get_all_possible_moves()

        best_move = None
        if self.is_maximizing:
            best_move_value = float('-inf')
        else:
            best_move_value = float('inf')

        for move in possible_moves:
            self.game.make_move(move[0], move[1], self.symbol)

            move_value = self.minimax(0, not self.is_maximizing, TicTacToe.get_other_player(self.symbol))
            if self.is_maximizing is True:
                if move_value > best_move_value:
                    best_move_value = move_value
                    best_move = move
            else:
                if move_value < best_move_value:
                    best_move_value = move_value
                    best_move = move

            self.game.undo_move(move[0], move[1], self.symbol)

        return best_move

    def minimax(self, depth: int, is_maximizing: bool, player_symbol: str) -> int:
        winner = TicTacToe.get_winner_for_board(self.game.board)

        if depth == self.max_depth or winner is not None:
            return self.calculate_score(winner, depth)
        else:
            if is_maximizing:
                best_score = float('-inf')
                all_possible_moves = self.game.get_all_possible_moves()

                for move in all_possible_moves:
                    self.game.make_move(move[0], move[1], player_symbol)
                    score = self.minimax(depth + 1, False, TicTacToe.get_other_player(player_symbol))
                    self.game.undo_move(move[0], move[1], player_symbol)
                    best_score = max(score, best_score)

                return best_score

            else:
                best_score = float('inf')
                all_possible_moves = self.game.get_all_possible_moves()

                for move in all_possible_moves:
                    self.game.make_move(move[0], move[1], player_symbol)
                    score = self.minimax(depth + 1, True, TicTacToe.get_other_player(player_symbol))
                    self.game.undo_move(move[0], move[1], player_symbol)
                    best_score = min(score, best_score)

                return best_score

    def calculate_score(self, winner: str, depth):
        lookup = {TicTacToe.FIRST: 10,
                  TicTacToe.TIE: 0,
                  TicTacToe.SECOND: -10}

        if depth == self.max_depth and winner is None:
            return self.heuristic_evaluation()
        else:
            return lookup[winner]

    def heuristic_evaluation(self):
        raise ValueError('WTF')
        # TODO finish this function
