import json
from collections import defaultdict
from CheckRules import CheckRules

class CheckHeuristic():
    @staticmethod
    def hasStonePatternInList(stone_list, search_list):
        for x, y in search_list:
            if (x, y) not in stone_list:
                return False
        return True

    @staticmethod
    def getPatternDict(stone_list, player, opponent, possible_moves, forbidden_move, player_captures, debug=False): 
        free_spots = possible_moves - forbidden_move[player]
        # free_spots_and_player_stones = free_spots | stone_list[player]
        left_diagonal_patterns, right_diagonal_patterns = list(), list()
        line_patterns, column_patterns = list(), list()
        string_len, low, high = 7, -3, 4

        ## get_line pattern
        captures = player_captures[player]
        for x, y in stone_list[player]:
            c1 = bytearray("." * string_len, 'utf-8')
            c2 = bytearray("." * string_len, 'utf-8')
            c3 = bytearray("." * string_len, 'utf-8')
            c4 = bytearray("." * string_len, 'utf-8')
            for i in range(low, high):
                if (x + i, y) in stone_list[player]:
                    c1[i + high - 1] = ord('X')
                elif (x + i, y) in stone_list[opponent]:
                    c1[i + high - 1] = ord('O')
                elif (x + i, y) in free_spots:
                    c1[i + high - 1] = ord("_")
            

        ## get column patter
                if (x, y + i) in stone_list[player]:
                    c2[i + high - 1] = ord('X')
                elif (x, y + i) in stone_list[opponent]:
                    c2[i + high - 1] = ord('O')
                elif (x, y + i) in free_spots:
                    c2[i + high - 1] = ord("_")

        ## get left diagonal pattern
                if (x + i, y + i) in stone_list[player]:
                    c3[i + high - 1] = ord('X')
                elif (x + i, y + i) in stone_list[opponent]:
                    c3[i + high - 1] = ord('O')
                elif (x + i, y + i) in free_spots:
                    c3[i + high - 1] = ord("_")

        ## get right diagonal pattern
                if (x - i, y + i) in stone_list[player]:
                    c4[i + high - 1] = ord('X')
                elif (x - i, y + i) in stone_list[opponent]:
                    c4[i + high - 1] = ord('O')
                elif (x - i, y + i) in free_spots:
                    c4[i + high - 1] = ord("_")

                captures += len(CheckRules._getCaptures(x, y, stone_list, player, opponent))
                
            line_patterns.append(c1)
            left_diagonal_patterns.append(c3)
            column_patterns.append(c2)
            right_diagonal_patterns.append(c4)

        dic = defaultdict(int)
        dic['captures'] = captures

        def countPattern(dic, patterns):
            if debug:
                print(patterns)
            for pattern in patterns:
                if bytearray(b"XXXXX") in pattern:
                    dic["fiveInRow"] += 1
                elif any(elem in pattern for elem in [bytearray(b"OXXXX_"), bytearray(b"_XXXXO")]):
                    dic["deadFour"] += 1
                elif any(elem in pattern for elem in [bytearray(b"_XXXX_"), bytearray(b"XXX_X"), bytearray(b"X_XXX"), bytearray(b"XX_XX")]):
                    dic["liveFour"] += 1
                elif any(elem in pattern for elem in [bytearray(b"OXXX__"), bytearray(b"__XXXO"), bytearray(b"OXX_X_"), bytearray(b"_X_XXO"), bytearray(b"OX_XX_"), bytearray(b"_XX_XO"), bytearray(b"O_XXX_O")]):
                    dic["deadThree"] += 1
                elif any(elem in pattern for elem in [bytearray(b"_XXX_"), bytearray(b"_XX_X"), bytearray(b"XX_X_"), bytearray(b"_X_XX"), bytearray(b"X_XX_"), bytearray(b"_XX__X"), bytearray(b"X__XX_"), bytearray(b"X_X_X")]):
                    dic["liveThree"] += 1
                elif any(elem in pattern for elem in [bytearray(b"OX__X_"), bytearray(b"_X__XO"), bytearray(b"OX_X__"), bytearray(b"__X_XO"), bytearray(b"OXX___"), bytearray(b"___XXO")]):
                    dic["deadTwo"] += 1
                elif any(elem in pattern for elem in [bytearray(b"X___X"), bytearray(b"X__X_"), bytearray(b"_X__X"), bytearray(b"_X_X_"), bytearray(b"__XX__")]):
                    dic["liveTwo"] += 1
                elif bytearray(b'__X__') in pattern:
                    dic["uselessOne"] += 1

        countPattern(dic, line_patterns)
        countPattern(dic, column_patterns)
        countPattern(dic, left_diagonal_patterns)
        countPattern(dic, right_diagonal_patterns)

        # print(json.dumps(dic, indent=4))

        return dic

