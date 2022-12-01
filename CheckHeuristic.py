import json

class CheckHeuristic():
    @staticmethod
    def hasStonePatternInList(stone_list, search_list):
        for x, y in search_list:
            if (x, y) not in stone_list:
                return False
        return True

    @staticmethod
    def getPatternDict(stone_list, player, opponent, possible_moves, forbidden_move): 
        free_spots = possible_moves - forbidden_move[player]
        free_spots_and_player_stones = free_spots | stone_list[player]
        right_diagonal_patterns = list()
        column_patterns = list()
        left_diagonal_patterns = list()
        line_patterns = list()
        string_len = 7
        low = -3
        high = 4
        ## get_line pattern
        for x, y in stone_list[player]:
            c1 = ["."] * string_len
            c2 = ["."] * string_len
            c3 = ["."] * string_len
            c4 = ["."] * string_len
            for i in range(low, high):
                c1[i + high - 1] = '.'
                if (x + i, y) in stone_list[player]:
                    c1[i + high - 1] = 'X'
                elif (x + i, y) in stone_list[opponent]:
                    c1[i + high - 1] = 'O'
                elif (x + i, y) in free_spots:
                    c1[i + high - 1] = "_"
            

        ## get column patter
                c2[i + high - 1] = '.'
                if (x, y + i) in stone_list[player]:
                    c2[i + high - 1] = 'X'
                elif (x, y + i) in stone_list[opponent]:
                    c2[i + high - 1] = 'O'
                elif (x, y + i) in free_spots:
                    c2[i + high - 1] = "_"

        ## get left diagonal pattern
                c3[i + high - 1] = '.'
                if (x + i, y + i) in stone_list[player]:
                    c3[i + high - 1] = 'X'
                elif (x + i, y + i) in stone_list[opponent]:
                    c3[i + high - 1] = 'O'
                elif (x + i, y + i) in free_spots:
                    c3[i + high - 1] = "_"

        ## get right diagonal pattern
                c4[i + high - 1] = '.'
                if (x - i, y + i) in stone_list[player]:
                    c4[i + high - 1] = 'X'
                elif (x - i, y + i) in stone_list[opponent]:
                    c4[i + high - 1] = 'O'
                elif (x - i, y + i) in free_spots:
                    c4[i + high - 1] = "_"
            line_patterns.append(''.join(c1))
            left_diagonal_patterns.append(''.join(c3))
            column_patterns.append(''.join(c2))
            right_diagonal_patterns.append(''.join(c4))

        dic = {
            "fiveInRow": 0,
            "liveFour": 0,
            "deadFour": 0,
            "liveThree": 0,
            "deadThree": 0,
            "liveTwo": 0,
            "deadTwo": 0,
        }

        def countPattern(dic, patterns):
            for pattern in patterns:
                if "XXXXX" in pattern:
                    dic["fiveInRow"] += 1
                elif any(elem in pattern for elem in ["OXXXX_", "_XXXXO"]):
                    dic["deadFour"] += 1
                elif any(elem in pattern for elem in ["_XXXX_", "XXX_X", "X_XXX", "XX_XX"]):
                    dic["liveFour"] += 1
                elif any(elem in pattern for elem in ["OXXX__", "__XXXO", "OXX_X_", "_X_XXO", "OX_XX_", "_XX_XO", "O_XXX_O"]):
                    dic["deadThree"] += 1
                elif any(elem in pattern for elem in ["_XXX_", "_XX_X", "XX_X_", "_X_XX", "X_XX_", "_XX__X", "X__XX_", "X_X_X"]):
                    dic["liveThree"] += 1
                elif any(elem in pattern for elem in ["_OX__X_", "_X__XO_", "OX_X__", "__X_XO", "OXX___", "___XXO"]):
                    dic["deadTwo"] += 1
                elif any(elem in pattern for elem in ["X___X", "X__X_", "_X__X", "_X_X_", "__XX__"]):
                    dic["liveTwo"] += 1

        countPattern(dic, line_patterns)
        countPattern(dic, column_patterns)
        countPattern(dic, left_diagonal_patterns)
        countPattern(dic, right_diagonal_patterns)

        # print(json.dumps(dic, indent=4))

        return dic


    # @staticmethod
    # def hasFiveInRow(stone_list, player, opponent, possible_moves, forbidden_move): 
    #     count = 0
    #     for x, y in stone_list[player]:
    #         # Check column
    #         if CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 1, y), (x + 2, y), (x + 3, y), (x + 4, y)]):
    #             count += 1
    #         # Check line
    #         if CheckHeuristic.hasStonePatternInList(stone_list[player], [(x, y + 1), (x, y + 2), (x, y + 3), (x, y + 4)]):
    #             count += 1
    #         # Check left diagonal
    #         if CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 1, y + 1), (x + 2, y + 2), (x + 3, y + 3), (x + 4, y + 4)]):
    #             count += 1
    #         # Check right diagonal
    #         if CheckHeuristic.hasStonePatternInList(stone_list[player], [(x - 1, y + 1), (x - 2, y + 2), (x - 3, y + 3), (x - 4, y - 4)]):
    #             count += 1
    #     return count

    # @staticmethod
    # def hasLiveFour(stone_list, player, opponent, possible_moves, forbidden_move):
    #     free_spots = possible_moves - forbidden_move[player]
    #     count = 0
    #     ### PATTERN _XXXX_
    #     for x, y in stone_list[player]:
    #         # Check column
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 1, y), (x + 2, y), (x + 3, y)])
    #             and (x - 1, y) in free_spots and (x + 4, y) in free_spots):
    #             count += 1
    #         # Check line
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x, y + 1), (x, y + 2), (x, y + 3)])
    #             and (x, y - 1) in free_spots and (x, y + 4) in free_spots):
    #             count += 1
    #         # Check left diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 1, y + 1), (x + 2, y + 2), (x + 3, y + 3)])
    #             and (x - 1, y - 1) in free_spots and (x + 4, y + 4) in free_spots):
    #             count += 1
    #     # Check right diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x - 1, y + 1), (x - 2, y + 2), (x - 3, y + 3)])
    #             and (x + 1, y - 1) in free_spots and (x - 4, y + 4) in free_spots):
    #             count += 1
    
    #     ### PATTERN XXX_X
    #         # Check column
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 1, y), (x + 2, y), (x + 4, y)])
    #             and (x + 3, y) in free_spots):
    #             count += 1
    #         # Check line
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x, y + 1), (x, y + 2), (x, y + 4)])
    #             and (x, y + 3) in free_spots):
    #             count += 1
    #         # Check left diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 1, y + 1), (x + 2, y + 2), (x + 4, y + 4)])
    #             and (x + 3, y + 3) in free_spots):
    #             count += 1
    #         # Check right diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x - 1, y + 1), (x - 2, y + 2), (x - 4, y + 4)])
    #             and (x - 3, y + 3) in free_spots):
    #             count += 1

    #     ### PATTERN X_XXX
    #         # Check column
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 2, y), (x + 3, y), (x + 4, y)])
    #             and (x + 1, y) in free_spots):
    #             count += 1
    #         # Check line
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x, y + 2), (x, y + 3), (x, y + 4)])
    #             and (x, y + 1) in free_spots):
    #             count += 1
    #         # Check left diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 2, y + 2), (x + 3, y + 3), (x + 4, y + 4)])
    #             and (x + 1, y + 1) in free_spots):
    #             count += 1
    #         # Check right diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x - 2, y + 2), (x - 3, y + 3), (x - 4, y + 4)])
    #             and (x - 1, y + 1) in free_spots):
    #             count += 1

    #     ### PATTERN XX_XX
    #         # Check column
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 1, y), (x + 3, y), (x + 4, y)])
    #             and (x + 2, y) in free_spots):
    #             count += 1
    #         # Check line
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x, y + 1), (x, y + 3), (x, y + 4)])
    #             and (x, y + 2) in free_spots):
    #             count += 1
    #         # Check left diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 1, y + 1), (x + 3, y + 3), (x + 4, y + 4)])
    #             and (x + 2, y + 2) in free_spots):
    #             count += 1
    #         # Check right diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x - 1, y + 1), (x - 3, y + 3), (x - 4, y + 4)])
    #             and (x - 2, y + 2) in free_spots):
    #             count += 1
            
    #     return count

    # @staticmethod
    # def hasDeadFour(stone_list, player, opponent, possible_moves, forbidden_move):
    #     free_spots = possible_moves - forbidden_move[player]
    #     free_spots_and_player_stones = free_spots | stone_list[player]
    #     count = 0
    #     ### CHECK PATTERN _XXXXO ^ OXXXX_
    #     # Check column
    #     for x, y in stone_list[player]:
    #         # Check column
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 1, y), (x + 2, y), (x + 3, y)])
    #             and (((x - 1, y) in free_spots) ^ ((x + 4, y) in free_spots))
    #             and (((x - 1, y) not in free_spots_and_player_stones) ^ ((x + 4, y) not in free_spots_and_player_stones))):
    #             count += 1
    #         # Check line
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x, y + 1), (x, y + 2), (x, y + 3)])
    #             and (((x, y - 1) in free_spots) ^ ((x, y + 4) in free_spots))
    #             and (((x, y - 1) not in free_spots_and_player_stones) ^ ((x, y + 4) not in free_spots_and_player_stones))):
    #             count += 1
    #         # Check left diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 1, y + 1), (x + 2, y + 2), (x + 3, y + 3)])
    #             and (((x - 1, y - 1) in free_spots) ^ ((x + 4, y + 4) in free_spots))
    #             and (((x - 1, y - 1) not in free_spots_and_player_stones) ^ ((x + 4, y + 4) not in free_spots_and_player_stones))):
    #             count += 1
    #         # Check right diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x - 1, y + 1), (x - 2, y + 2), (x - 3, y + 3)])
    #             and (((x + 1, y - 1) in free_spots) ^ ((x - 4, y + 4) in free_spots))
    #             and (((x + 1, y - 1) not in free_spots_and_player_stones) ^ ((x - 4, y + 4) not in free_spots_and_player_stones))):
    #             count += 1
    #     return count

    # @staticmethod
    # def hasLiveThree(stone_list, player, opponent, possible_moves, forbidden_move):
    #     free_spots = possible_moves - forbidden_move[player]
    #     count = 0
    #     ### PATTERN _XXX_
    #     for x, y in stone_list[player]:
    #         # Check column
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 1, y), (x + 2, y)])
    #             and (x - 1, y) in free_spots and (x + 3, y) in free_spots):
    #             count += 1
    #         # Check line
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x, y + 1), (x, y + 2)])
    #             and (x, y - 1) in free_spots and (x, y + 3) in free_spots):
    #             count += 1
    #         # Check left diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 1, y + 1), (x + 2, y + 2)])
    #             and (x - 1, y - 1) in free_spots and (x + 3, y + 3) in free_spots):
    #             count += 1
    #     # Check right diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x - 1, y + 1), (x - 2, y + 2)])
    #             and (x + 1, y - 1) in free_spots and (x - 3, y + 3) in free_spots):
    #             count += 1

    #     ### PATTERN X_XX
    #         # Check column
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 2, y), (x + 3, y)])
    #             and (x + 1, y) in free_spots):
    #             count += 1
    #         # Check line
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x, y + 2), (x, y + 3)])
    #             and (x, y + 1) in free_spots):
    #             count += 1
    #         # Check left diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 2, y + 2), (x + 3, y + 3)])
    #             and (x + 1, y + 1) in free_spots):
    #             count += 1
    #     # Check right diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x - 2, y + 2), (x - 3, y + 3)])
    #             and (x - 1, y + 1) in free_spots):
    #             count += 1

    #     ### PATTERN XX_X
    #         # Check column
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 1, y), (x + 3, y)])
    #             and (x + 2, y) in free_spots):
    #             count += 1
    #         # Check line
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x, y + 1), (x, y + 3)])
    #             and (x, y + 2) in free_spots):
    #             count += 1
    #         # Check left diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 1, y + 1), (x + 3, y + 3)])
    #             and (x + 2, y + 2) in free_spots):
    #             count += 1
    #     # Check right diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x - 1, y + 1), (x - 3, y + 3)])
    #             and (x - 2, y + 2) in free_spots):
    #             count += 1

    #     ### PATTERN XX__X
    #         # Check column
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 1, y), (x + 4, y)])
    #             and (x + 2, y) in free_spots and (x + 3, y) in free_spots):
    #             count += 1
    #         # Check line
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x, y + 1), (x, y + 4)])
    #             and (x, y + 2) in free_spots and (x, y + 3) in free_spots):
    #             count += 1
    #         # Check left diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 1, y + 1), (x + 4, y + 4)])
    #             and (x + 2, y + 2) in free_spots and (x + 3, y + 3) in free_spots):
    #             count += 1
    #         # Check right diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x - 1, y + 1), (x - 4, y + 4)])
    #             and (x - 2, y + 2) in free_spots and (x - 3, y + 3) in free_spots):
    #             count += 1

    #     ### PATTERN X__XX
    #         # Check column
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 3, y), (x + 4, y)])
    #             and (x + 1, y) in free_spots and (x + 2, y) in free_spots):
    #             count += 1
    #         # Check line
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x, y + 3), (x, y + 4)])
    #             and (x, y + 1) in free_spots and (x, y + 2) in free_spots):
    #             count += 1
    #         # Check left diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 3, y + 3), (x + 4, y + 4)])
    #             and (x + 1, y + 1) in free_spots and (x + 2, y + 2) in free_spots):
    #             count += 1
    #         # Check right diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x - 3, y + 3), (x - 4, y + 4)])
    #             and (x - 1, y + 1) in free_spots and (x - 2, y + 2) in free_spots):
    #             count += 1

    #     ### PATTERN X_X_X
    #         # Check column
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 2, y), (x + 4, y)])
    #             and (x + 1, y) in free_spots and (x + 3, y) in free_spots):
    #             count += 1
    #         # Check line
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x, y + 2), (x, y + 4)])
    #             and (x, y + 1) in free_spots and (x, y + 3) in free_spots):
    #             count += 1
    #         # Check left diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 2, y + 2), (x + 4, y + 4)])
    #             and (x + 1, y + 1) in free_spots and (x + 3, y + 3) in free_spots):
    #             count += 1
    #         # Check right diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x - 2, y + 2), (x - 4, y + 4)])
    #             and (x - 1, y + 1) in free_spots and (x - 3, y + 3) in free_spots):
    #             count += 1
    #     return count

    # @staticmethod
    # def hasDeadThree(stone_list, player, opponent, possible_moves, forbidden_move):
    #     free_spots = possible_moves - forbidden_move[player]
    #     free_spots_and_player_stones = free_spots | stone_list[player]
    #     count = 0
    #     ### CHECK PATTERN OXXX_
    #     for x, y in stone_list[player]:
    #         # Check column
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 1, y), (x + 2, y)])
    #             and (((x - 1, y) in free_spots) ^ ((x + 3, y) in free_spots))
    #             and (((x - 1, y) not in free_spots_and_player_stones) ^ ((x + 3, y) not in free_spots_and_player_stones))):
    #             count += 1
    #         # Check line
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x, y + 1), (x, y + 2)])
    #             and (((x, y - 1) in free_spots) ^ ((x, y + 3) in free_spots))
    #             and (((x, y - 1) not in free_spots_and_player_stones) ^ ((x, y + 3) not in free_spots_and_player_stones))):
    #             count += 1
    #         # Check left diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 1, y + 1), (x + 2, y + 2)])
    #             and (((x - 1, y - 1) in free_spots) ^ ((x + 3, y + 3) in free_spots))
    #             and (((x - 1, y - 1) not in free_spots_and_player_stones) ^ ((x + 3, y + 3) not in free_spots_and_player_stones))):
    #             count += 1
    #         # Check right diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x - 1, y + 1), (x - 2, y + 2)])
    #             and (((x + 1, y - 1) in free_spots) ^ ((x - 3, y + 3) in free_spots))
    #             and (((x + 1, y - 1) not in free_spots_and_player_stones) ^ ((x - 3, y + 3) not in free_spots_and_player_stones))):
    #             count += 1

    #     ### CHECK PATTERN OXX_X ^ XX_XO
    #         # Check column
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 1, y), (x + 3, y)])
    #             and (x + 2, y) in free_spots and ((x - 1, y) not in free_spots_and_player_stones) ^ ((x + 4, y) not in free_spots_and_player_stones)):
    #             count += 1
    #         # Check line
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x, y + 1), (x, y + 3)])
    #             and (x, y + 2) in free_spots and ((x, y - 1) not in free_spots_and_player_stones) ^ ((x, y + 4) not in free_spots_and_player_stones)):
    #             count += 1
    #         # Check left diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 1, y + 1), (x + 3, y + 3)])
    #             and (x + 2, y + 2) in free_spots and ((x - 1, y - 1) not in free_spots_and_player_stones) ^ ((x + 4, y + 4) not in free_spots_and_player_stones)):
    #             count += 1
    #         # Check right diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x - 1, y + 1), (x - 3, y + 3)])
    #             and (x - 2, y + 2) in free_spots and ((x + 1, y - 1) not in free_spots_and_player_stones) ^ ((x - 4, y + 4) not in free_spots_and_player_stones)):
    #             count += 1

    #     ### CHECK PATTERN X_XXO ^ OX_XX
    #         # Check column
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 2, y), (x + 3, y)])
    #             and (x + 1, y) in free_spots and ((x + 4, y) not in free_spots_and_player_stones) ^ ((x - 1, y) not in free_spots_and_player_stones)):
    #             count += 1
    #         # Check line
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x, y + 2), (x, y + 3)])
    #             and (x, y + 4) in free_spots and ((x, y + 4) not in free_spots_and_player_stones) ^ ((x, y - 1) not in free_spots_and_player_stones)):
    #             count += 1
    #         # Check left diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 2, y + 2), (x + 3, y + 3)])
    #             and (x + 1, y + 1) in free_spots and ((x + 4, y + 4) not in free_spots_and_player_stones) ^ ((x - 1, y - 1) not in free_spots_and_player_stones)):
    #             count += 1
    #         # Check right diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x - 2, y + 2), (x - 3, y + 3)])
    #             and (x - 1, y + 1) in free_spots and ((x - 4, y + 4) not in free_spots_and_player_stones)  ^ ((x + 1, y - 1) not in free_spots_and_player_stones)):
    #             count += 1

    #     ### CHECK PATTERN O_XXX_O
    #         # Check column
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 1, y), (x + 2, y)])
    #             and (x - 1, y) in free_spots and (x + 3, y) in free_spots
    #             and (x - 2, y) not in free_spots_and_player_stones and (x + 4, y) not in free_spots_and_player_stones):
    #             count += 1
    #         # Check line
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x, y + 1), (x, y + 2)])
    #             and (x, y - 1) in free_spots and (x, y + 3) in free_spots
    #             and (x, y - 2) not in free_spots_and_player_stones and (x, y + 4) not in free_spots_and_player_stones):
    #             count += 1
    #         # Check left diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 1, y + 1), (x + 2, y + 2)])
    #             and (x - 1, y - 1) in free_spots and (x + 3, y + 3) in free_spots
    #             and (x - 2, y - 2) not in free_spots_and_player_stones and (x + 4, y + 4) not in free_spots_and_player_stones):
    #             count += 1
    #         # Check right diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x - 1, y + 1), (x - 2, y + 2)])
    #             and (x + 1, y - 1) in free_spots and (x - 3, y + 3) in free_spots
    #             and (x + 2, y - 2) not in free_spots_and_player_stones and (x - 4, y + 4) not in free_spots_and_player_stones):
    #             count += 1

    #     return count


    # @staticmethod
    # def hasLiveTwo(stone_list, player, opponent, possible_moves, forbidden_move):
    #     free_spots = possible_moves - forbidden_move[player]
    #     free_spots_and_player_stones = free_spots | stone_list[player]
    #     count = 0
    #     ### CHECK PATTERN X___X
    #     for x, y in stone_list[player]:
    #         # Check column
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 4, y)])
    #             and (x + 1, y) in free_spots and (x + 2, y) in free_spots and (x + 3, y) in free_spots):
    #             count += 1
    #         # Check line
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x, y + 4)])
    #             and (x, y + 1) in free_spots and (x, y + 2) in free_spots and (x, y + 3) in free_spots):
    #             count += 1
    #         # Check left diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 4, y + 4)])
    #             and (x + 1, y + 1) in free_spots and (x + 2, y + 2) in free_spots and (x + 3, y + 3) in free_spots):
    #             count += 1
    #         # Check right diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x - 4, y + 4)])
    #             and (x - 1, y + 1) in free_spots and (x - 2, y + 2) in free_spots and (x - 3, y + 3) in free_spots):
    #             count += 1

    #     ### CHECK PATTERN _X__X_
    #         # Check column
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 3, y)])
    #             and (x + 1, y) in free_spots and (x + 2, y) in free_spots and (x - 1, y) in free_spots and (x + 4, y) in free_spots):
    #             count += 1
    #         # Check line
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x, y + 3)])
    #             and (x, y + 1) in free_spots and (x, y + 2) in free_spots and (x, y - 1) in free_spots and (x, y + 4) in free_spots):
    #             count += 1
    #         # Check left diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 3, y + 3)])
    #             and (x + 1, y + 1) in free_spots and (x + 2, y + 2) in free_spots and (x - 1, y - 1) in free_spots and (x + 4, y + 4) in free_spots):
    #             count += 1
    #         # Check right diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x - 3, y + 3)])
    #             and (x - 1, y + 1) in free_spots and (x - 2, y + 2) in free_spots and (x + 1, y - 1) in free_spots and (x - 4, y + 4) in free_spots):
    #             count += 1

    #     ### CHECK PATTERN _X_X_
    #         # Check column
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 2, y)])
    #             and (x + 1, y) in free_spots and (x - 1, y) in free_spots and (x + 3, y) in free_spots):
    #             count += 1
    #         # Check line
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x, y + 2)])
    #             and (x, y + 1) in free_spots and (x, y - 1) in free_spots and (x, y + 3) in free_spots):
    #             count += 1
    #         # Check left diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 2, y + 2)])
    #             and (x + 1, y + 1) in free_spots and (x - 1, y - 1) in free_spots and (x + 3, y + 3) in free_spots):
    #             count += 1
    #         # Check right diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x - 2, y + 2)])
    #             and (x - 1, y + 1) in free_spots and (x + 1, y - 1) in free_spots and (x - 3, y + 3) in free_spots):
    #             count += 1

    #     ### CHECK PATTERN _XX_
    #         # Check column
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 1, y)])
    #             and (x - 1, y) in free_spots and (x + 2, y) in free_spots):
    #             count += 1
    #         # Check line
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x, y + 1)])
    #             and (x, y - 1) in free_spots and (x, y + 2) in free_spots):
    #             count += 1
    #         # Check left diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 1, y + 1)])
    #             and (x - 1, y - 1) in free_spots and (x + 2, y + 2) in free_spots):
    #             count += 1
    #         # Check right diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x - 1, y + 1)])
    #             and (x + 1, y - 1) in free_spots and (x - 2, y + 2) in free_spots):
    #             count += 1
        
    #     return count


    # @staticmethod
    # def hasDeadTwo(stone_list, player, opponent, possible_moves, forbidden_move):
    #     free_spots = possible_moves - forbidden_move[player]
    #     free_spots_and_player_stones = free_spots | stone_list[player]
    #     count = 0
    #     ### CHECK PATTERN OXX_ ^ _XXO
    #     for x, y in stone_list[player]:
    #         # Check column
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 1, y)])
    #             and ((x - 1, y) not in free_spots_and_player_stones and (x + 2, y) in free_spots)
    #             ^ ((x + 2, y) not in free_spots_and_player_stones and (x - 1, y) in free_spots)):
    #             count += 1
    #         # Check line
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x, y + 1)])
    #             and ((x, y - 1) not in free_spots_and_player_stones and (x, y + 2) in free_spots)
    #             ^ ((x, y + 2) not in free_spots_and_player_stones and (x, y - 1) in free_spots)):
    #             count += 1
    #         # Check left diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 1, y + 1)])
    #             and ((x - 1, y - 1) not in free_spots_and_player_stones and (x + 2, y + 2) in free_spots)
    #             ^ ((x + 2, y + 2) not in free_spots_and_player_stones and (x - 1, y - 1) in free_spots)):
    #             count += 1
    #         # Check right diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x - 1, y + 1)])
    #             and ((x + 1, y - 1) not in free_spots_and_player_stones and (x - 2, y + 2) in free_spots)
    #             ^ ((x - 2, y + 2) not in free_spots_and_player_stones and (x + 1, y - 1) in free_spots)):
    #             count += 1

    #     ### CHECK PATTERN OX_X ^ X_XO
    #         # Check column
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 2, y)])
    #             and (x + 1, y) in free_spots
    #             and ((x - 1, y) not in free_spots_and_player_stones) ^ ((x + 3, y) not in free_spots_and_player_stones)):
    #             count += 1
    #         # Check line
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x, y + 2)])
    #             and (x, y + 1) in free_spots
    #             and ((x, y - 1) not in free_spots_and_player_stones) ^ ((x, y + 3) not in free_spots_and_player_stones)):
    #             count += 1
    #         # Check left diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 2, y + 2)])
    #             and (x + 1, y + 1) in free_spots
    #             and ((x - 1, y - 1) not in free_spots_and_player_stones) ^ ((x + 3, y + 3) not in free_spots_and_player_stones)):
    #             count += 1
    #         # Check right diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x - 2, y + 2)])
    #             and (x - 1, y + 1) in free_spots
    #             and ((x + 1, y - 1) not in free_spots_and_player_stones) ^ ((x - 3, y + 3) not in free_spots_and_player_stones)):
    #             count += 1

    #     ### CHECK PATTERN OX__X ^ X__XO
    #         # Check column
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 3, y)])
    #             and (x + 1, y) in free_spots and (x + 2, y) in free_spots
    #             and ((x - 1, y) not in free_spots_and_player_stones) ^ ((x + 4, y) not in free_spots_and_player_stones)):
    #             count += 1
    #         # Check line
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x, y + 3)])
    #             and (x, y + 1) in free_spots and (x, y + 2) in free_spots
    #             and ((x, y - 1) not in free_spots_and_player_stones) ^ ((x, y + 4) not in free_spots_and_player_stones)):
    #             count += 1
    #         # Check left diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x + 3, y + 3)])
    #             and (x + 1, y + 1) in free_spots and (x + 2, y + 2) in free_spots
    #             and ((x - 1, y - 1) not in free_spots_and_player_stones) ^ ((x + 4, y + 4) not in free_spots_and_player_stones)):
    #             count += 1
    #         # Check right diagonal
    #         if (CheckHeuristic.hasStonePatternInList(stone_list[player], [(x - 3, y + 3)])
    #             and (x - 1, y + 1) in free_spots and (x - 2, y + 2) in free_spots
    #             and ((x + 1, y - 1) not in free_spots_and_player_stones) ^ ((x - 4, y + 4) not in free_spots_and_player_stones)):
    #             count += 1
        
    #     return count