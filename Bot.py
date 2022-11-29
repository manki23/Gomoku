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


    @staticmethod
    def getNextMove(possible_moves, stone_list, player, opponent, forbidden_move):
        start = perf_counter()
        # best_move = [-1, -1, -1]
        minimize_opponent = [inf, inf, inf]
        # CheckHeuristic.getPatternString(stone_list, player, opponent, possible_moves, forbidden_move)

        best_move = (-1, -1)
        original_depth = 3
        alpha, beta = -inf, inf
        def minimax(stone_list, p, depth, alpha, beta):
            nonlocal best_move
            if depth == 0:
                return Bot.getBoardEval(stone_list, opponent if p == player else p, p, possible_moves, forbidden_move)
            visited = set()
            if p == player:
                max_eval = 0
                # print(possible_moves)
                for move in possible_moves:
                    if move not in visited:
                        visited.add(move)
                        stone_list[player].add(move)
                        possible_moves.remove(move)

                        score = minimax(stone_list, opponent, depth - 1, alpha, beta)
                        # print(f"{depth} >>> pl:", move, score)
                        if alpha <= score and depth == original_depth:
                            best_move = move

                        alpha = max(alpha, score)

                        stone_list[player].remove(move)
                        possible_moves.add(move)
                        if alpha >= beta: break
                return alpha
            else:
                min_eval = inf
                for move in possible_moves:
                    if move not in visited:
                        visited.add(move)
                        stone_list[opponent].add(move)
                        possible_moves.remove(move)

                        score = -minimax(stone_list, player, depth - 1, alpha, beta)
                        # print(f"{depth} >>> op:", move, score)

                        stone_list[opponent].remove(move)
                        possible_moves.add(move)
                        beta = min(beta, score)
                        if alpha >= beta: break
                return beta

        minimax(stone_list, player, original_depth, alpha, beta)
        # print(best_move)

        # for x, y in possible_moves - forbidden_move[player]:
        #     # PLAY MOVE
        #     stone_list[player].add((x, y))
        #     possible_moves.remove((x, y))

        #     my_value = Bot.getBoardEval(stone_list, player, opponent, possible_moves, forbidden_move)
        #     opponent_value = Bot.getBoardEval(stone_list, opponent, player, possible_moves, forbidden_move)
        #     my_value += 10_000 * len(CheckRules._getCaptures(x, y, stone_list, player, opponent))
        #     if my_value > best_move[-1] and opponent_value < minimize_opponent[-1]:
        #         best_move = [x, y, my_value]
        #         minimize_opponent = [x, y, opponent_value]

        #     # REVERSE MOVE
        #     stone_list[player].remove((x, y))
        #     possible_moves.add((x, y))
        print(f'\rTIME : {perf_counter() - start}', end='')

        return best_move