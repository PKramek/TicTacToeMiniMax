import itertools

from TicTacToe.player import RandomPlayer
from TicTacToe.tictactoe import TicTacToe

tictactoe_game = TicTacToe()

player_1 = RandomPlayer(tictactoe_game)
player_2 = RandomPlayer(tictactoe_game)

# iterator used for convenient player selection for next round
players = itertools.cycle([(player_1, TicTacToe.FIRST), (player_2, TicTacToe.SECOND)])

wins_dict = {TicTacToe.FIRST: 0,
             TicTacToe.SECOND: 0,
             TicTacToe.TIE: 0}

for i in range(1000):

    tictactoe_game.reset_game()

    while not tictactoe_game.is_over():
        player, player_sign = next(players)
        move_x, move_y = player.chose_move()
        tictactoe_game.make_move(move_x, move_y, player_sign)
    tictactoe_game.is_over()
    wins_dict[tictactoe_game.winner] += 1

print(wins_dict)
