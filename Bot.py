from math import inf
from random import choice
from CheckHeuristic import CheckHeuristic
from time import perf_counter
from CheckRules import CheckRules
from copy import deepcopy


class Bot():

    def displayBoard(game):
        board = [['.' for _ in range(19)] for _ in range(19)]
        for x, y in game.stone_list[game.player]:
            board[y][x] = 'X'
        for x, y in game.stone_list[game.opponent]:
            board[y][x] = 'O'
        for x, y in game.possible_moves:
            board[y][x] = '*'
        for line in board:
            print('\t', ''.join(line))

    @staticmethod
    def getBoardEval(bot_game):

        # start = perf_counter()
        dic = CheckHeuristic.getPatternDict(bot_game)
        # print(f'\rTIME CheckHeuristic: {perf_counter() - start}', end='')
        # print()

        # start = perf_counter()
        dicOpp = CheckHeuristic.getPatternDict(bot_game)

        # print(f'\rTIME CheckHeuristicOpp : {perf_counter() - start}', end='')


        score = (600000 * (dic["fiveInRow"] - dicOpp["fiveInRow"]) +
                 10_000 * (dic["liveFour"] - dicOpp["liveFour"]) +
                 1100 * (dic["deadFour"] - dicOpp["deadFour"]) +
                 900 * (dic["liveThree"] - dicOpp["liveThree"]) +
                 500 * (dic["deadThree"] - dicOpp["deadThree"]) +
                 50 * (dic["liveTwo"] - dicOpp["liveTwo"]) +
                 10 * (dic["deadTwo"] - dicOpp["deadTwo"]) -
                 10 * (dic["uselessOne"] - dicOpp["uselessOne"]) +
                 5_000 * (dic["captures"] - dicOpp["captures"])
                 )

        return score

    @staticmethod
    def getNextMove(game, debug=False):
        start = perf_counter()

        best_move = (-1, -1)
        a, b = -inf, inf
        original_depth = 3
        alpha, beta = -inf, inf
        debug_arr = [[0 for _ in range(19)] for _ in range(19)]
        visitedNodes = 0

        game_copy = deepcopy(game)

        def minimax(bot_game, depth, alpha, beta):
            nonlocal best_move
            nonlocal a, b, visitedNodes
            if depth == 0:
                # bot_player = p
                # bot_opponent = game.opponent if p == game.player else game.player
                boardEval = Bot.getBoardEval(bot_game)

                return boardEval
            visited = set()
            if bot_game.player == game.player:
                for move in bot_game.playable_area:
                    if move not in visited:
                        visitedNodes += 1
                        visited.add(move)

                        #  PLAY ONE MOVE
                        bot_game.stone_list[player].add(move)
                        bot_game.playable_area.remove(move)
                        # p_moves.remove(move)

                        score = minimax(bot_game.stone_list, bot_game.playable_area, opponent,
                                        depth - 1, alpha, beta)
                        if depth == original_depth:
                            debug_arr[move[1]][move[0]] = f'{score}'

                        if alpha < score and depth == original_depth:
                            best_move = move

                        # REMOVE LAST MOVE
                        bot_game.stone_list[player].remove(move)
                        bot_game.playable_area.add(move)
                        # p_moves.add(move)

                        if alpha >= beta:
                            return alpha

                        a = alpha = max(alpha, score)

                return alpha
            else:
                for move in bot_game.playable_area:
                    if move not in visited:
                        visitedNodes += 1
                        visited.add(move)
                        bot_game.stone_list[opponent].add(move)
                        bot_game.playable_area.remove(move)
                        # p_moves.remove(move)

                        score = -minimax(bot_game.stone_list, bot_game.playable_area, player,
                                         depth - 1, alpha, beta)

                        # debug_arr[move[1]][move[0]] = f'{score}:{depth}'

                        bot_game.stone_list[opponent].remove(move)
                        bot_game.playable_area.add(move)
                        # p_moves.add(move)

                        if beta <= alpha:
                            return beta

                        b = beta = min(beta, score)
                return beta

        minimax(game_copy, original_depth, alpha, beta)

        if debug == True:
            # print("DECISION:", best_move, a, b)
            # print('VISITED NODES:', visitedNodes)
            for x, y in game.stone_list[game.player]:
                debug_arr[y][x] = '[X]'
            for x, y in game.stone_list[game.opponent]:
                debug_arr[y][x] = '[O]'

            for line in debug_arr:
                for elem in line:
                    print(f"{elem:>8}", end=" ")
                print()

        print(f'\rTIME : {perf_counter() - start}', end='')

        return best_move
