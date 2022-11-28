from math import inf
from random import choice
from CheckHeuristic import CheckHeuristic
from time import perf_counter
from CheckRules import CheckRules

class Bot():

    @staticmethod
    def getBoardEval(stone_list, player, opponent, possible_moves, forbidden_move):
        args = (stone_list, player, opponent, possible_moves, forbidden_move)
        hasFiveInRow = CheckHeuristic.hasFiveInRow(*args)
        if hasFiveInRow: print("\nFIVE IN ROW:", hasFiveInRow)
        hasLiveFour = CheckHeuristic.hasLiveFour(*args)
        hasDeadFour = CheckHeuristic.hasDeadFour(*args)
        hasLiveThree = CheckHeuristic.hasLiveThree(*args)
        hasDeadThree = CheckHeuristic.hasDeadThree(*args)
        hasLiveTwo = CheckHeuristic.hasLiveTwo(*args)
        hasDeadTwo = CheckHeuristic.hasDeadTwo(*args)

        return 100_000 * hasFiveInRow + 15_000 * hasLiveFour + 1_500 * hasDeadFour + 10_000 * hasLiveThree + 5_000 * hasDeadThree + 50 * hasLiveTwo + 10 * hasDeadTwo

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