from math import inf
from random import choice
from CheckHeuristic import CheckHeuristic
from time import perf_counter
from CheckRules import CheckRules

class Bot():

    def displayBoard(stone_list, player, opponent, possible_moves):
        board = [['.' for _ in range(19)] for _ in range(19)]
        for x, y in stone_list[player]:
            board[y][x] = 'X'
        for x, y in stone_list[opponent]:
            board[y][x] = 'O'
        for x, y in possible_moves:
            board[y][x] = '*'
        for line in board:
            print('\t', ''.join(line))

    @staticmethod
    def getBoardEval(stone_list, player, opponent, possible_moves, forbidden_move):

        dic = CheckHeuristic.getPatternDict(stone_list, player, opponent, possible_moves, forbidden_move)
        dicOpp = CheckHeuristic.getPatternDict(stone_list, opponent, player, possible_moves, forbidden_move)

        score = (60000 * (dic["fiveInRow"] - dicOpp["fiveInRow"]) + 
                 4800 * (dic["liveFour"] - dicOpp["liveFour"]) +
                 500 * (dic["deadFour"] - dicOpp["deadFour"]) +
                 500 * (dic["liveThree"] - dicOpp["liveThree"]) +
                 200 * (dic["deadThree"] - dicOpp["deadThree"]) +
                 50 * (dic["liveTwo"] - dicOpp["liveTwo"]) +
                 10 * (dic["deadTwo"] - dicOpp["deadTwo"]))


        #score = 1_000_000 * dic["fiveInRow"] + 15_000 * dic["liveFour"] + 1_500 * dic["deadFour"] + 10_000 * dic["liveThree"] + 5_000 * dic["deadThree"] + 50 * dic["liveTwo"] + 10 * dic["deadTwo"]
        return score


    @staticmethod
    def getNextMove(possible_moves, stone_list, player, opponent, forbidden_move, p_moves):
        start = perf_counter()
        # best_move = [-1, -1, -1]
        # minimize_opponent = [inf, inf, inf]
        # CheckHeuristic.getPatternString(stone_list, player, opponent, possible_moves, forbidden_move)

        best_move = (-1, -1)
        original_depth = 3
        alpha, beta = -inf, inf
        def minimax(stone_list, p, depth, alpha, beta):
            nonlocal best_move
            if depth == 0:
                boardEval = Bot.getBoardEval(stone_list, opponent if p == player else p, p, p_moves, forbidden_move) 
                # boardEval = Bot.getBoardEval(stone_list, player, opponent, p_moves, forbidden_move) 
                return boardEval
            visited = set()
            if p == player:
                max_eval = 0
                for move in possible_moves:
                    if move not in visited:
                        visited.add(move)
                        stone_list[player].add(move)
                        possible_moves.remove(move)
                        p_moves.remove(move)

                        score = minimax(stone_list, opponent, depth - 1, alpha, beta)
                        # print(f"{depth} >>> pl:", move, score)
                        #Bot.displayBoard(stone_list, opponent if p == player else p, p, possible_moves)
                        if alpha <= score and depth == original_depth:
                            best_move = move

                        alpha = max(alpha, score)

                        stone_list[player].remove(move)
                        possible_moves.add(move)
                        p_moves.add(move)
                        if alpha >= beta: break
                return alpha
            else:
                min_eval = inf
                for move in possible_moves:
                    if move not in visited:
                        visited.add(move)
                        stone_list[opponent].add(move)
                        possible_moves.remove(move)
                        p_moves.remove(move)

                        score = -minimax(stone_list, player, depth - 1, alpha, beta)
                        # print(f"{depth} >>> op:", move, score)

                        stone_list[opponent].remove(move)
                        possible_moves.add(move)
                        p_moves.add(move)
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