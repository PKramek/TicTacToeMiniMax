import itertools
from random import seed

from TicTacToe.game_tree import GameTree
from TicTacToe.players import MiniMaxPlayer
from TicTacToe.tictactoe import TicTacToe

tictactoe_game = TicTacToe()

seed(42)

player_1 = MiniMaxPlayer(tictactoe_game, TicTacToe.FIRST, 20)
player_2 = MiniMaxPlayer(tictactoe_game, TicTacToe.SECOND, 20)
# player_1 = RandomPlayer(tictactoe_game, TicTacToe.FIRST)
# player_2 = RandomPlayer(tictactoe_game, TicTacToe.SECOND)

game_tree = GameTree(tictactoe_game.board, player_1.symbol)

# iterator used for convenient player selection for next round
players = itertools.cycle([player_1, player_2])

wins_dict = {TicTacToe.FIRST: 0,
             TicTacToe.SECOND: 0,
             TicTacToe.TIE: 0}

for i in range(1):
    tictactoe_game.reset_game()

    while not tictactoe_game.is_over():
        player = next(players)
        move = player.chose_move()
        tictactoe_game.make_move(move, player.symbol)
        game_tree.make_move(move, player.symbol)

    wins_dict[tictactoe_game.winner] += 1

print(wins_dict)
