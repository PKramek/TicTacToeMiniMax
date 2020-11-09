import itertools

from TicTacToe.players import RandomPlayer, MiniMaxPlayer
from TicTacToe.tictactoe import TicTacToe

tictactoe_game = TicTacToe()

# player_2 = RandomPlayer(tictactoe_game, TicTacToe.SECOND)
player_1 = MiniMaxPlayer(tictactoe_game, TicTacToe.FIRST, 20)
player_2 = MiniMaxPlayer(tictactoe_game, TicTacToe.SECOND, 20)

# iterator used for convenient player selection for next round
players = itertools.cycle([player_1, player_2])

wins_dict = {TicTacToe.FIRST: 0,
             TicTacToe.SECOND: 0,
             TicTacToe.TIE: 0}

for i in range(20):
    tictactoe_game.reset_game()

    while not tictactoe_game.is_over():
        player = next(players)
        move_x, move_y = player.chose_move()
        tictactoe_game.make_move(move_x, move_y, player.symbol)
    wins_dict[tictactoe_game.winner] += 1

print(wins_dict)
