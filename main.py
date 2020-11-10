import itertools
from time import time

from TicTacToe.game_tree import GameTree
from TicTacToe.players import HeuristicMiniMaxTreePlayer, MiniMaxTreePlayer
from TicTacToe.tictactoe import TicTacToe

tictactoe_game = TicTacToe()
game_tree = GameTree(tictactoe_game.board, TicTacToe.FIRST)

# tree_player_1 = RandomTreePlayer(game_tree, TicTacToe.FIRST)
# tree_player_2 = RandomTreePlayer(game_tree, TicTacToe.SECOND)

tree_player_1 = HeuristicMiniMaxTreePlayer(game_tree, TicTacToe.FIRST, 3)
# tree_player_2 = HeuristicMiniMaxTreePlayer(game_tree, TicTacToe.SECOND, 3)

tree_player_2 = MiniMaxTreePlayer(game_tree, TicTacToe.SECOND)

wins_dict = {TicTacToe.FIRST_SYMBOL: 0,
             TicTacToe.SECOND_SYMBOL: 0,
             TicTacToe.TIE_SYMBOL: 0}

time_start = time()
for i in range(5):
    players = itertools.cycle([tree_player_1, tree_player_2])
    tictactoe_game.reset_game()
    game_tree.reset(tictactoe_game.board)

    while not tictactoe_game.is_over():
        player = next(players)
        move = player.chose_move()
        game_tree.make_move(move, player.symbol)
        tictactoe_game.make_move(move, player.symbol)

    wins_dict[tictactoe_game.winner] += 1
time_end = time()

print(time_end - time_start)
print(wins_dict)
