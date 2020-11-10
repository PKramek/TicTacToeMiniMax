from abc import ABC, abstractmethod
from random import choice as random_choice
from typing import Tuple

from TicTacToe.game_tree import GameTree, Node
from TicTacToe.tictactoe import TicTacToe


class TreePlayer(ABC):
    def __init__(self, game_tree: GameTree, symbol: str):
        self.game_tree = game_tree
        self.symbol = symbol

    @abstractmethod
    def chose_move(self) -> Tuple[int, int]:
        pass


class RandomTreePlayer(TreePlayer):

    def chose_move(self) -> Tuple[int, int]:
        possible_moves = self.game_tree.get_roots_children()
        move = random_choice(possible_moves).move

        return move


class HeuristicMiniMaxTreePlayer(TreePlayer):
    maximizing_lookup = {TicTacToe.FIRST: True,
                         TicTacToe.SECOND: False}

    def __init__(self, game_tree: GameTree, symbol: str, max_depth: int):
        super().__init__(game_tree, symbol)
        self.max_depth = max_depth
        self.is_maximizing = HeuristicMiniMaxTreePlayer.maximizing_lookup[self.symbol]

    def chose_move(self) -> Tuple[int, int]:
        possible_moves = self.game_tree.get_roots_children()

        best_move = None
        if self.is_maximizing:
            best_move_value = float('-inf')
        else:
            best_move_value = float('inf')

        for move in possible_moves:
            move_value = self.minimax_tree(move, 0, not self.is_maximizing, TicTacToe.get_other_player(self.symbol))
            if self.is_maximizing is True:
                if move_value > best_move_value:
                    best_move_value = move_value
                    best_move = move
            else:
                if move_value < best_move_value:
                    best_move_value = move_value
                    best_move = move

        return best_move.move

    def minimax_tree(self, tree_node: Node, depth: int, is_maximizing: bool, player_symbol: str) -> int:
        winner = TicTacToe.get_winner_for_board(tree_node.board)

        if depth == self.max_depth or winner is not None:
            return self.calculate_score(winner, depth)
        else:
            if is_maximizing:
                best_score = float('-inf')
                all_possible_moves = tree_node.children

                for move in all_possible_moves:
                    score = self.minimax_tree(move, depth + 1, False, TicTacToe.get_other_player(player_symbol))
                    best_score = max(score, best_score)

                return best_score

            else:
                best_score = float('inf')
                all_possible_moves = tree_node.children

                for move in all_possible_moves:
                    score = self.minimax_tree(move, depth + 1, True, TicTacToe.get_other_player(player_symbol))
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
        raise NotImplemented()
        # TODO finish this function


class MiniMaxTreePlayer(TreePlayer):
    maximizing_lookup = {TicTacToe.FIRST: True,
                         TicTacToe.SECOND: False}

    def __init__(self, game_tree: GameTree, symbol: str):
        super().__init__(game_tree, symbol)
        self.is_maximizing = MiniMaxTreePlayer.maximizing_lookup[self.symbol]

    def chose_move(self) -> Tuple[int, int]:
        possible_moves = self.game_tree.get_roots_children()

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

        return best_move.move

    def minimax_tree(self, tree_node: Node, is_maximizing: bool, player_symbol: str) -> int:
        winner = TicTacToe.get_winner_for_board(tree_node.board)

        if winner is not None:
            return self.calculate_score(winner)
        else:
            if is_maximizing:
                best_score = float('-inf')
                all_possible_moves = tree_node.children

                for move in all_possible_moves:
                    score = self.minimax_tree(move, False, TicTacToe.get_other_player(player_symbol))
                    best_score = max(score, best_score)

                return best_score

            else:
                best_score = float('inf')
                all_possible_moves = tree_node.children

                for move in all_possible_moves:
                    score = self.minimax_tree(move, True, TicTacToe.get_other_player(player_symbol))
                    best_score = min(score, best_score)

                return best_score

    def calculate_score(self, winner: str):
        lookup = {TicTacToe.FIRST: 10,
                  TicTacToe.TIE: 0,
                  TicTacToe.SECOND: -10}

        return lookup[winner]
