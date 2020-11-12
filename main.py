import itertools
from time import time
from typing import Optional

from TicTacToe.game_tree import GameTree
from TicTacToe.players import HeuristicMiniMaxTreePlayerV2, RandomTreePlayer, MiniMaxTreePlayerV2
from TicTacToe.tictactoe import TicTacToe


class Experiment:
    RANDOM = "Random"
    MINIMAX = "MINIMAX"
    HEURISTIC_MINIMAX = "HEURISTIC"

    FIRST_EXECUTION_TIME = "First execution time"
    SECOND_EXECUTION_TIME = "Second execution time"

    def __init__(self, first_player_type: str, second_player_type: str, num_repetitions: int,
                 first_heuristic_depth: Optional[int] = 10,
                 second_heuristic_depth: Optional[int] = 10):
        players_class_lookup = {self.RANDOM: RandomTreePlayer,
                                self.MINIMAX: MiniMaxTreePlayerV2,
                                self.HEURISTIC_MINIMAX: HeuristicMiniMaxTreePlayerV2
                                }
        self._results = {}
        self.num_repetitions = num_repetitions
        self.tictactoe = TicTacToe()
        self.game_tree = GameTree(self.tictactoe.board, TicTacToe.FIRST)

        if first_player_type not in players_class_lookup.keys():
            raise ValueError('Not defined first player type')

        if second_player_type not in players_class_lookup.keys():
            raise ValueError('Not defined second player type')

        first_class = players_class_lookup[first_player_type]
        second_class = players_class_lookup[second_player_type]

        if first_player_type == self.HEURISTIC_MINIMAX:
            self.first_player = first_class(self.game_tree, TicTacToe.FIRST, first_heuristic_depth)
        else:
            self.first_player = first_class(self.game_tree, TicTacToe.FIRST)

        if second_player_type == self.HEURISTIC_MINIMAX:
            self.second_player = second_class(self.game_tree, TicTacToe.SECOND, second_heuristic_depth)
        else:
            self.second_player = second_class(self.game_tree, TicTacToe.SECOND)

        self._results = None

        self.reset_results()

    def reset_results(self):
        self._results = {
            TicTacToe.FIRST_SYMBOL: 0,
            TicTacToe.SECOND_SYMBOL: 0,
            TicTacToe.TIE_SYMBOL: 0,
            self.FIRST_EXECUTION_TIME: 0,
            self.SECOND_EXECUTION_TIME: 0
        }

    def play_games(self):

        for _ in range(self.num_repetitions):
            players_iterator = itertools.cycle([(self.first_player, self.FIRST_EXECUTION_TIME),
                                                (self.second_player, self.SECOND_EXECUTION_TIME)])
            self.tictactoe.reset_game()
            self.game_tree.reset(self.tictactoe.board)

            while not self.tictactoe.is_over():
                player, player_exec_time_results_key = next(players_iterator)

                time_start = time()
                move = player.chose_move()
                self._results[player_exec_time_results_key] += time() - time_start

                self.game_tree.make_move(move, player.symbol)
                self.tictactoe.make_move(move, player.symbol)


            self._results[self.tictactoe.winner] += 1

    def get_formatted_results(self):
        formatted_results = {"First won": self._results[TicTacToe.FIRST_SYMBOL],
                             "Second won": self._results[TicTacToe.SECOND_SYMBOL],
                             "Ties": self._results[TicTacToe.TIE_SYMBOL],
                             "First execution time": round(self._results[self.FIRST_EXECUTION_TIME], 2),
                             "Second execution time": round(self._results[self.SECOND_EXECUTION_TIME], 2)}

        return formatted_results


# if __name__ == "__main__":
#     program_exec_time_start = time()
#
#     experiments_results = {"random_vs_minimax": None,
#                            "random_vs_heuristic": {},
#                            "minimax_vs_heuristic": {}
#                            }
#     num_of_games = 1
#
#
#
#     random_vs_minimax = Experiment(Experiment.RANDOM, Experiment.MINIMAX, num_repetitions=num_of_games)
#     random_vs_minimax.play_games()
#
#     results = random_vs_minimax.get_formatted_results()
#     experiments_results["random_vs_minimax"] = results
#     print("Random vs Minimax")
#     print(results)
#
#     print("\nRandom vs Heuristic MiniMax")
#     for i in range(1, 10):  # TODO make sure that max depth is 9
#         random_vs_heuristic_minimax = Experiment(Experiment.RANDOM, Experiment.HEURISTIC_MINIMAX,
#                                                  num_repetitions=num_of_games, second_heuristic_depth=i)
#         random_vs_heuristic_minimax.play_games()
#         results = random_vs_heuristic_minimax.get_formatted_results()
#         experiments_results["random_vs_heuristic"][str(i)] = results
#         print("Max depth: {}, results: {}".format(i, results))
#
#     print("\nMinimax vs Heuristic MiniMax")
#     for i in range(1, 10):  # TODO make sure that max depth is 9
#         minimax_vs_heuristic_minimax = Experiment(Experiment.MINIMAX, Experiment.HEURISTIC_MINIMAX,
#                                                   num_repetitions=num_of_games, second_heuristic_depth=i)
#         minimax_vs_heuristic_minimax.play_games()
#         results = minimax_vs_heuristic_minimax.get_formatted_results()
#         experiments_results["minimax_vs_heuristic"][str(i)] = results
#         print("Max depth: {}, results: {}".format(i, results))
#
#     print("\nProgram execution time: {}".format(time() - program_exec_time_start))

num_of_games = 2
minimax_vs_heuristic_minimax = Experiment(Experiment.HEURISTIC_MINIMAX, Experiment.MINIMAX,
                                          num_repetitions=num_of_games, first_heuristic_depth=5,
                                          second_heuristic_depth=20)
minimax_vs_heuristic_minimax.play_games()
results = minimax_vs_heuristic_minimax.get_formatted_results()
print(results)
