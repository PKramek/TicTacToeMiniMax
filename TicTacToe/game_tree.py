from __future__ import annotations

from typing import Tuple, List, Optional

from TicTacToe.tictactoe import TicTacToe


class Node:
    def __init__(self, board: List[List[str]], move: Optional[Tuple[int, int]], player_symbol: str):
        self.board = board
        self.move = move
        self.player_symbol = player_symbol
        self._children = None

    # Lazy object creation
    @property
    def children(self) -> List[Node]:
        """
        This property allows for lazy creation of children for node.

        :return: List[Node]
        """
        if self._children is None:
            self._children = []

            possible_moves = TicTacToe.get_all_possible_moves_for_board(self.board)

            for possible_move in possible_moves:
                next_player_symbol = TicTacToe.get_other_player(self.player_symbol)
                board_after_move = TicTacToe.get_board_state_after_move_for_board(
                    possible_move[0],
                    possible_move[1],
                    next_player_symbol,
                    self.board
                )
                self.children.append(Node(board_after_move, possible_move, next_player_symbol))

        return self._children

    def get_child_with_move(self, move: Tuple[int, int]) -> Optional[Node]:
        """
        Returns a child with Node with specified move, if no child was found None is returned.

        :param move: Tuple with information what move was made
        :type move: Tuple[int, int]
        :return: Optional[Node]
        """
        for child in self.children:
            if child.move == move:
                return child
        return None


class GameTree:
    """
    This class represents game tree
    """

    def __init__(self, starting_board: List[List[str]], first_player_symbol):
        # first node does not have a move
        self.root = Node(starting_board, None, first_player_symbol)

    def make_move(self, move: Tuple[int, int], player_symbol: str) -> None:
        """
        This method moves root of the tree to a node with a given move, this way tree always represents current
        board
        :param player_symbol: Symbol of a player performing move
        :type player_symbol: str
        :param move: Move to be made on the board
        :type move: Tuple[int, int]
        """
        new_root = self.root.get_child_with_move(move)
        if new_root is None:
            raise ValueError('Move not possible')
        if new_root.player_symbol != player_symbol:
            raise ValueError('It is not {} turn'.format(player_symbol))

    def get_root(self) -> Node:
        return self.root
