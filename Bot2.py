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
        dic = CheckHeuristic.getPatternDict(bot_game, bot_game.player, bot_game.opponent)
        # print(f'\rTIME CheckHeuristic: {perf_counter() - start}', end='')
        # print()

        # start = perf_counter()
        dicOpp = CheckHeuristic.getPatternDict(bot_game, bot_game.opponent, bot_game.player)

        # print(f'\rTIME CheckHeuristicOpp : {perf_counter() - start}', end='')

        # print(dic)
        # print(dicOpp)
        # input()
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
        best_move = None
        best_score = -inf

        debug_arr = [[0 for _ in range(19)] for _ in range(19)]
        alpha, beta = -inf, inf

        # game_copy = deepcopy(game)
        # game_copy.bot_mode = True

        def minimax(bot_game, depth, alpha, beta, maximizingPlayer):
            if depth == 0 or bot_game.gameover:
                boardEval = Bot.getBoardEval(bot_game)
                # print(boardEval)
                return boardEval

            # bestScore = -inf if maximizingPlayer else inf

            for move in bot_game.playable_area.copy():
                # print("aqui", move, bestScore, best_score, maximizingPlayer)

                #  PLAY ONE MOVE
                bot_game.playOneMove(*move)

                score = minimax(bot_game, depth - 1, alpha, beta, not maximizingPlayer)
                #if maximizingPlayer:
                #    score = -score 


                # REMOVE LAST MOVE
                bot_game.revertLastMove()

                if maximizingPlayer:
                    # bestScore = max(bestScore, score)
                    alpha = max(alpha, score)
                else:
                    # bestScore = min(bestScore, score)
                    beta = min(beta, score)

                if beta <= alpha:
                    return alpha if maximizingPlayer else beta

            return alpha if maximizingPlayer else beta

        game_copy = deepcopy(game)
        for move in game_copy.playable_area.copy():

            #  PLAY ONE MOVE
            game_copy.playOneMove(*move)
            #print("iter", Bot.getBoardEval(game_copy))
            # input()

            score = minimax(game_copy, 3, alpha, beta, False)
            #print(move, score)
            # input(">>")
            debug_arr[move[1]][move[0]] = f'{score}'

            # REMOVE LAST MOVE
            game_copy.revertLastMove()

            if score > best_score:
                best_score = score
                best_move = move
                alpha = max(alpha, best_score)
            # if score < beta:
            #     beta = min(beta, score)

            if alpha >= beta:
                break

        if debug == False:
            for x, y in game.stone_list[game.player]:
                debug_arr[y][x] = '[X]'
            for x, y in game.stone_list[game.opponent]:
                debug_arr[y][x] = '[O]'

            for line in debug_arr:
                for elem in line:
                    print(f"{elem:>8}", end=" ")
                print()

        print(f'\rTIME : {perf_counter() - start}', end='')
        game.bot_move = best_move
        return best_move
