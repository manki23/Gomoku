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

        dic = CheckHeuristic.getPatternDict(
            stone_list, player, opponent, possible_moves, forbidden_move, player_captures)
        dicOpp = CheckHeuristic.getPatternDict(
            stone_list, opponent, player, possible_moves, forbidden_move, player_captures)

        score = (100000 * (dic["fiveInRow"] - dicOpp["fiveInRow"]) +
                 4800 * (dic["liveFour"] - dicOpp["liveFour"]) +
                 500 * (dic["deadFour"] - dicOpp["deadFour"]) +
                 500 * (dic["liveThree"] - dicOpp["liveThree"]) +
                 200 * (dic["deadThree"] - dicOpp["deadThree"]) +
                 50 * (dic["liveTwo"] - dicOpp["liveTwo"]) +
                 10 * (dic["deadTwo"] - dicOpp["deadTwo"]) -
                 10 * (dic["uselessOne"] - dicOpp["uselessOne"]) +
                 10_000 * (dic["captures"] - dicOpp["captures"])
                 )

        #score = 1_000_000 * dic["fiveInRow"] + 15_000 * dic["liveFour"] + 1_500 * dic["deadFour"] + 10_000 * dic["liveThree"] + 5_000 * dic["deadThree"] + 50 * dic["liveTwo"] + 10 * dic["deadTwo"]
        return score

    @staticmethod
    def getNextMove(playable_area, stone_list, player, opponent, forbidden_move, p_moves, player_captures):
        start = perf_counter()
        # best_move = [-1, -1, -1]
        # minimize_opponent = [inf, inf, inf]
        # CheckHeuristic.getPatternString(stone_list, player, opponent, playable_area, forbidden_move)

        best_move = (-1, -1)
        a, b = -inf, inf
        original_depth = 3
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
                max_score = -inf
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

                        if max_score < score and depth == original_depth:
                            best_move = move

                        max_score = max(score, max_score)

                        # if alpha <= score and depth == original_depth:
                        #    best_move = move
                        #    print(f"tour: {player}", alpha)

                        stone_list[player].remove(move)
                        playable_area.add(move)
                        p_moves.add(move)

                        if score >= beta:
                            return max_score

                        a = alpha = max(alpha, score)
                        # if alpha < beta:
                        #    break
                return max_score
            else:
                min_score = inf
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

                        min_score = min(min_score, score)

                        stone_list[opponent].remove(move)
                        playable_area.add(move)
                        p_moves.add(move)

                        if score <= alpha:
                            return min_score

                        b = beta = min(beta, score)
                        # if alpha >= beta:
                        #    break
                return min_score

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
