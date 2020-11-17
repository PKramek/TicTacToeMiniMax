from abc import ABC, abstractmethod
from random import choice as random_choice, sample
from typing import Tuple

from numpy import array as np_array, multiply as np_multiply, sum as np_sum

from TicTacToe.game_tree import GameTree, Node
from TicTacToe.tictactoe import TicTacToe


class Player(ABC):
    def __init__(self, game_tree: GameTree, symbol: str):
        self.game_tree = game_tree
        self.symbol = symbol

    @abstractmethod
    def chose_move(self) -> Tuple[int, int]:
        pass

    def set_symbol(self, symbol):
        self.symbol = symbol


class RandomPlayer(Player):

    def chose_move(self) -> Tuple[int, int]:
        possible_moves = self.game_tree.get_roots_children()
        move = random_choice(possible_moves).move

        return move


class MiniMaxBase(Player):
    maximizing_lookup = {TicTacToe.FIRST: True,
                         TicTacToe.SECOND: False}

    def __init__(self, game_tree: GameTree, symbol: str):
        super().__init__(game_tree, symbol)
        self.is_maximizing = MiniMaxBase.maximizing_lookup[self.symbol]

    def chose_move(self) -> Tuple[int, int]:
        roots_children = self.game_tree.get_roots_children()
        possible_moves = sample(roots_children, len(roots_children))

        best_move = None
        if self.is_maximizing:
            best_move_value = float('-inf')
        else:
            best_move_value = float('inf')

        for move in possible_moves:
            move_value = self.minimax_tree(move, not self.is_maximizing, TicTacToe.get_other_player(self.symbol))
            if self.is_maximizing is True:
                if move_value > best_move_value:
                    best_move_value = move_value
                    best_move = move
            else:
                if move_value < best_move_value:
                    best_move_value = move_value
                    best_move = move
        if best_move is None:
            raise RuntimeError()
        return best_move.move

    @abstractmethod
    def minimax_tree(self, tree_node: Node, is_maximizing: bool, player_symbol: str) -> int:
        pass


class MiniMaxPlayer(MiniMaxBase):
    def minimax_tree(self, tree_node: Node, is_maximizing: bool, player_symbol: str) -> int:
        return self.recurrent_minimax(tree_node, is_maximizing, player_symbol)

    def recurrent_minimax(self, tree_node: Node, is_maximizing: bool, player_symbol: str) -> int:
        winner = TicTacToe.get_winner_for_board(tree_node.board)

        if winner is not None:
            return self.calculate_score(winner)
        else:
            if is_maximizing:
                best_score = float('-inf')
                all_possible_moves = sample(tree_node.children, len(tree_node.children))

                for move in all_possible_moves:
                    score = self.recurrent_minimax(move, False, TicTacToe.get_other_player(player_symbol))
                    best_score = max(score, best_score)

                return best_score

            else:
                best_score = float('inf')
                all_possible_moves = tree_node.children

                for move in all_possible_moves:
                    score = self.recurrent_minimax(move, True, TicTacToe.get_other_player(player_symbol))
                    best_score = min(score, best_score)

                return best_score

    def calculate_score(self, winner: int):
        lookup = {TicTacToe.FIRST: 10,
                  TicTacToe.TIE: 0,
                  TicTacToe.SECOND: -10}

        return lookup[winner]


class HeuristicMiniMaxPlayer(MiniMaxBase):

    def __init__(self, game_tree: GameTree, symbol: str, max_depth: int):
        super().__init__(game_tree, symbol)
        if isinstance(max_depth, int) and 1 <= max_depth:
            self.max_depth = max_depth
        else:
            raise ValueError("Max depth must be integer bigger than 1")

    @staticmethod
    def heuristic_evaluation(board):
        heuristic_matrix = np_array([[3, 2, 3], [2, 4, 2], [3, 2, 3]])

        return np_sum(np_multiply(board, heuristic_matrix))

    def minimax_tree(self, tree_node: Node, is_maximizing: bool, player_symbol: str) -> int:
        return self.recurrent_minimax(tree_node, 0, is_maximizing, player_symbol)

    def recurrent_minimax(self, tree_node: Node, depth: int, is_maximizing: bool, player_symbol: str) -> int:
        winner = TicTacToe.get_winner_for_board(tree_node.board)

        if depth >= self.max_depth or winner is not None:
            return self.calculate_score(winner, depth, tree_node.board)
        else:
            if is_maximizing:
                best_score = float('-inf')
                all_possible_moves = sample(tree_node.children, len(tree_node.children))

                for move in all_possible_moves:
                    score = self.recurrent_minimax(move, depth + 1, False, TicTacToe.get_other_player(player_symbol))
                    best_score = max(score, best_score)

                return best_score

            else:
                best_score = float('inf')
                all_possible_moves = tree_node.children

                for move in all_possible_moves:
                    score = self.recurrent_minimax(move, depth + 1, True, TicTacToe.get_other_player(player_symbol))
                    best_score = min(score, best_score)

                return best_score

    def calculate_score(self, winner: int, depth: int, board):
        lookup = {TicTacToe.FIRST: 10,
                  TicTacToe.TIE: 0,
                  TicTacToe.SECOND: -10}

        if depth == self.max_depth and winner is None:
            return self.heuristic_evaluation(board)
        else:
            return lookup[winner]
