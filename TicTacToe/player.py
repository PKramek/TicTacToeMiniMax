from abc import ABC, abstractmethod
from random import choice as random_choice
from typing import Tuple

import TicTacToe


class Player(ABC):
    def __init__(self, game: TicTacToe):
        self.game = game

    @abstractmethod
    def chose_move(self) -> Tuple[int, int]:
        pass


class RandomPlayer(Player):

    def chose_move(self) -> Tuple[int, int]:
        possible_moves = self.game.get_all_possible_moves()
        move = random_choice(possible_moves)

        return move


class MiniMaxPlayer(Player):

    def chose_move(self) -> Tuple[int, int]:
        possible_moves = self.game.get_all_possible_moves_for_board()
        move = self.minimax()

        return move

    def minimax(self) -> Tuple[int, int]:
        pass
