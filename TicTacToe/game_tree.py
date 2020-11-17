from __future__ import annotations

from typing import Tuple, List, Optional

from TicTacToe.tictactoe import TicTacToe


class Node:
    # To speedup access to fields of objects and reduce RAM usage
    __slots__ = ['board', 'move', 'player_symbol', '_children']

    def __init__(self, board: List[List[int]], move: Optional[Tuple[int, int]], player_symbol: str):
        self.board = board
        self.move = move
        self.player_symbol = player_symbol
        self._children = None

    @property
    def children(self) -> List[Node]:

        if self._children is None:
            self._children = []

            possible_moves = TicTacToe.get_all_possible_moves_for_board(self.board)
            next_player_symbol = TicTacToe.get_other_player(self.player_symbol)

            for possible_move in possible_moves:
                board_after_move = TicTacToe.get_board_state_after_move_for_board(
                    possible_move[0],
                    possible_move[1],
                    next_player_symbol,
                    self.board
                )
                self.children.append(Node(board_after_move, possible_move, next_player_symbol))

        return self._children

    def get_child_with_move(self, move: Tuple[int, int]) -> Optional[Node]:
        for child in self.children:
            if child.move == move:
                return child
        return None


class GameTree:

    def __init__(self, starting_board: List[List[int]], first_player_symbol):
        # first node does not have a move, and symbol must be other than the first player
        self.start_symbol = TicTacToe.get_other_player(first_player_symbol)
        self.root = Node(starting_board, None, self.start_symbol)

    def make_move(self, move: Tuple[int, int], player_symbol: str) -> None:
        new_root = self.root.get_child_with_move(move)
        if new_root is None:
            raise ValueError('Move not possible')
        if new_root.player_symbol != player_symbol:
            raise ValueError('It is not ' + player_symbol + ' turn')
        self.root = new_root

    def get_root(self) -> Node:
        return self.root

    def get_roots_children(self) -> List[Node]:
        return self.root.children

    def reset(self, starting_board: List[List[int]], first_player_symbol: str):
        self.start_symbol = TicTacToe.get_other_player(first_player_symbol)
        self.root = Node(starting_board, None, self.start_symbol)

