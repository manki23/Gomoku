from math import inf
from random import choice
from CheckHeuristic import CheckHeuristic
from time import perf_counter
from CheckRules import CheckRules

class Bot():

    @staticmethod
    def getBoardEval(stone_list, player, opponent, possible_moves, forbidden_move):

        dic = CheckHeuristic.getPatternDict(stone_list, player, opponent, possible_moves, forbidden_move)

        score = 1_000_000 * dic["fiveInRow"] + 15_000 * dic["liveFour"] + 1_500 * dic["deadFour"] + 10_000 * dic["liveThree"] + 5_000 * dic["deadThree"] + 50 * dic["liveTwo"] + 10 * dic["deadTwo"]
        return score

    # @staticmethod
    # def minimax(stone_list, player, depth):
    #     if depth == 0

    @staticmethod
    def getNextMove(possible_moves, stone_list, player, opponent, forbidden_move):
        start = perf_counter()
        best_move = [-1, -1, -1]
        minimize_opponent = [inf, inf, inf]
        # CheckHeuristic.getPatternString(stone_list, player, opponent, possible_moves, forbidden_move)
        for x, y in possible_moves - forbidden_move[player]:
            # PLAY MOVE
            stone_list[player].add((x, y))
            possible_moves.remove((x, y))

            my_value = Bot.getBoardEval(stone_list, player, opponent, possible_moves, forbidden_move)
            opponent_value = Bot.getBoardEval(stone_list, opponent, player, possible_moves, forbidden_move)
            my_value += 10_000 * len(CheckRules._getCaptures(x, y, stone_list, player, opponent))
            if my_value > best_move[-1] and opponent_value < minimize_opponent[-1]:
                best_move = [x, y, my_value]
                minimize_opponent = [x, y, opponent_value]

            # REVERSE MOVE
            stone_list[player].remove((x, y))
            possible_moves.add((x, y))
        print(f'\rTIME : {perf_counter() - start}', end='')

        return (best_move[0], best_move[1])