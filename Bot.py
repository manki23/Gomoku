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
    def getBoardEval(stone_list, player, opponent, possible_moves, forbidden_move, player_captures):

        # start = perf_counter()
        dic = CheckHeuristic.getPatternDict(
            stone_list, player, opponent, possible_moves, forbidden_move, player_captures)
        # print(f'\rTIME CheckHeuristic: {perf_counter() - start}', end='')
        # print()

        # start = perf_counter()
        dicOpp = CheckHeuristic.getPatternDict(
            stone_list, opponent, player, possible_moves, forbidden_move, player_captures)

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
    def getNextMove(playable_area, stone_list, player, opponent, forbidden_move, p_moves, player_captures):
        start = perf_counter()

        best_move = (-1, -1)
        a, b = -inf, inf
        original_depth = 4
        alpha, beta = -inf, inf
        debug_arr = [[0 for _ in range(19)] for _ in range(19)]
        visitedNodes = 0

        def minimax(stone_list, p, depth, alpha, beta):
            nonlocal best_move
            nonlocal a, b, visitedNodes
            if depth == 0:
                # boardEval = Bot.getBoardEval(
                #    stone_list, opponent if p == player else player, p, p_moves, forbidden_move, player_captures)
                boardEval = Bot.getBoardEval(
                    stone_list, p, opponent if p == player else player, playable_area, forbidden_move, player_captures)
                # boardEval = Bot.getBoardEval(stone_list, player, opponent, p_moves, forbidden_move, player_captures)
                return boardEval
            visited = set()
            if p == player:
                for move in playable_area:
                    if move not in visited:
                        visitedNodes += 1
                        visited.add(move)
                        stone_list[player].add(move)
                        playable_area.remove(move)
                        p_moves.remove(move)

                        score = minimax(stone_list, opponent,
                                        depth - 1, alpha, beta)
                        if depth == original_depth:
                            debug_arr[move[1]][move[0]] = f'{score}'

                        if alpha < score and depth == original_depth:
                            best_move = move


                        stone_list[player].remove(move)
                        playable_area.add(move)
                        p_moves.add(move)

                        if alpha >= beta:
                            return alpha

                        a = alpha = max(alpha, score)

                return alpha
            else:
                for move in playable_area:
                    if move not in visited:
                        visitedNodes += 1
                        visited.add(move)
                        stone_list[opponent].add(move)
                        playable_area.remove(move)
                        p_moves.remove(move)

                        score = -minimax(stone_list, player,
                                         depth - 1, alpha, beta)

                        # debug_arr[move[1]][move[0]] = f'{score}:{depth}'

                        stone_list[opponent].remove(move)
                        playable_area.add(move)
                        p_moves.add(move)

                        if beta <= alpha:
                            return beta

                        b = beta = min(beta, score)
                return beta

        minimax(
            stone_list, player, original_depth, alpha, beta)
        print('VISITED NODES:', visitedNodes)
        print("DECISION:", best_move, a, b)
        for x, y in stone_list[player]:
            debug_arr[y][x] = '[X]'
        for x, y in stone_list[opponent]:
            debug_arr[y][x] = '[O]'

        for line in debug_arr:
            for elem in line:
                print(f"{elem:>8}", end=" ")
            print()

        print(f'\rTIME : {perf_counter() - start}', end='')

        return best_move
