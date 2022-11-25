class CheckHeuristic():
    @staticmethod
    def hasStonePatternInList(stone_list, search_list):
        for x, y in search_list:
            if (x, y) not in stone_list:
                return False
        return True

    @staticmethod
    def hasFiveInRow(stone_list, player, opponent, possible_moves, forbidden_move):
        count = 0
        for x, y in stone_list[player]:
            # Check column
            if hasStonePatternInList(stone_list[player], [(x + 1, y), (x + 2, y), (x + 3, y), (x + 4, y)]):
                count += 1
            # Check line
            if hasStonePatternInList(stone_list[player], [(x, y + 1), (x, y + 2), (x, y + 3), (x, y + 4)]):
                count += 1
            # Check left diagonal
            if hasStonePatternInList(stone_list[player], [(x + 1, y + 1), (x + 2, y + 2), (x + 3, y + 3), (x + 4, y + 4)]):
                count += 1
            # Check right diagonal
            if hasStonePatternInList(stone_list[player], [(x - 1, y + 1), (x - 2, y + 2), (x - 3, y + 3), (x - 4, y - 4)]):
                count += 1
        return count

    @staticmethod
    def hasLiveFour(stone_list, player, opponent, possible_moves, forbidden_move):
        free_spots = possible_moves - forbidden_move[player]
        count = 0
        ### PATTERN _XXXX_
        for x, y in stone_list[player]:
            # Check column
            if (hasStonePatternInList(stone_list[player], [(x + 1, y), (x + 2, y), (x + 3, y)])
                and (x - 1, y) in free_spots and (x + 4, y) in free_spots):
                count += 1
            # Check line
            if (hasStonePatternInList(stone_list[player], [(x, y + 1), (x, y + 2), (x, y + 3)])
                and (x, y - 1) in free_spots and (x, y + 4) in free_spots):
                count += 1
            # Check left diagonal
            if (hasStonePatternInList(stone_list[player], [(x + 1, y + 1), (x + 2, y + 2), (x + 3, y + 3)])
                and (x - 1, y - 1) in free_spots and (x + 4, y + 4) in free_spots):
                count += 1
        # Check right diagonal
            if (hasStonePatternInList(stone_list[player], [(x - 1, y + 1), (x - 2, y + 2), (x - 3, y + 3)])
                and (x + 1, y - 1) in free_spots and (x - 4, y + 4) in free_spots):
                count += 1
    
        ### PATTERN XXX_X
        for x, y in stone_list[player]:
            # Check column
            if (hasStonePatternInList(stone_list[player], [(x + 1, y), (x + 2, y), (x + 4, y)])
                and (x + 3, y) in free_spots):
                count += 1
            # Check line
            if (hasStonePatternInList(stone_list[player], [(x, y + 1), (x, y + 2), (x, y + 4)])
                and (x, y + 3) in free_spots):
                count += 1
            # Check left diagonal
            if (hasStonePatternInList(stone_list[player], [(x + 1, y + 1), (x + 2, y + 2), (x + 4, y + 4)])
                and (x + 3, y + 3) in free_spots):
                count += 1
            # Check right diagonal
            if (hasStonePatternInList(stone_list[player], [(x - 1, y + 1), (x - 2, y + 2), (x - 4, y + 4)])
                and (x - 3, y + 3) in free_spots):
                count += 1

        ### PATTERN X_XXX
        for x, y in stone_list[player]:
            # Check column
            if (hasStonePatternInList(stone_list[player], [(x + 2, y), (x + 3, y), (x + 4, y)])
                and (x + 1, y) in free_spots):
                count += 1
            # Check line
            if (hasStonePatternInList(stone_list[player], [(x, y + 2), (x, y + 3), (x, y + 4)])
                and (x, y + 1) in free_spots):
                count += 1
            # Check left diagonal
            if (hasStonePatternInList(stone_list[player], [(x + 2, y + 2), (x + 3, y + 3), (x + 4, y + 4)])
                and (x + 1, y + 1) in free_spots):
                count += 1
            # Check right diagonal
            if (hasStonePatternInList(stone_list[player], [(x - 2, y + 2), (x - 3, y + 3), (x - 4, y + 4)])
                and (x - 1, y + 1) in free_spots):
                count += 1

        ### PATTERN XX_XX
        for x, y in stone_list[player]:
            # Check column
            if (hasStonePatternInList(stone_list[player], [(x + 1, y), (x + 3, y), (x + 4, y)])
                and (x + 2, y) in free_spots):
                count += 1
            # Check line
            if (hasStonePatternInList(stone_list[player], [(x, y + 1), (x, y + 3), (x, y + 4)])
                and (x, y + 2) in free_spots):
                count += 1
            # Check left diagonal
            if (hasStonePatternInList(stone_list[player], [(x + 1, y + 1), (x + 3, y + 3), (x + 4, y + 4)])
                and (x + 2, y + 2) in free_spots):
                count += 1
            # Check right diagonal
            if (hasStonePatternInList(stone_list[player], [(x - 1, y + 1), (x - 3, y + 3), (x - 4, y + 4)])
                and (x - 2, y + 2) in free_spots):
                count += 1
            
        return count

    @staticmethod
    def hasDeadFour(stone_list, player, opponent, possible_moves, forbidden_move):
        free_spots = possible_moves - forbidden_move[player]
        free_spots_and_player_stones = free_spots | stone_list[player]
        count = 0
        ### CHECK PATTERN _XXXXO
        # Check column
        for x, y in stone_list[player]:
            # Check column
            if (hasStonePatternInList(stone_list[player], [(x + 1, y), (x + 2, y), (x + 3, y)])
                and (((x - 1, y) in free_spots) ^ ((x + 4, y) in free_spots))
                and (((x - 1, y) not in free_spots_and_player_stones) ^ ((x + 4, y) not in free_spots_and_player_stones))):
                count += 1
            # Check line
            if (hasStonePatternInList(stone_list[player], [(x, y + 1), (x, y + 2), (x, y + 3)])
                and (((x, y - 1) in free_spots) ^ ((x, y + 4) in free_spots))
                and (((x, y - 1) not in free_spots_and_player_stones) ^ ((x, y + 4) not in free_spots_and_player_stones))):
                count += 1
            # Check left diagonal
            if (hasStonePatternInList(stone_list[player], [(x + 1, y + 1), (x + 2, y + 2), (x + 3, y + 3)])
                and (((x - 1, y - 1) in free_spots) ^ ((x + 4, y + 4) in free_spots))
                and (((x - 1, y - 1) not in free_spots_and_player_stones) ^ ((x + 4, y + 4) not in free_spots_and_player_stones))):
                count += 1
            # Check right diagonal
            if (hasStonePatternInList(stone_list[player], [(x - 1, y + 1), (x - 2, y + 2), (x - 3, y + 3)])
                and (((x + 1, y - 1) in free_spots) ^ ((x - 4, y + 4) in free_spots))
                and (((x + 1, y - 1) not in free_spots_and_player_stones) ^ ((x - 4, y + 4) not in free_spots_and_player_stones))):
                count += 1
        return count

    @staticmethod
    def hasLiveThree(stone_list, player, opponent, possible_moves, forbidden_move):
        free_spots = possible_moves - forbidden_move[player]
        count = 0
        ### PATTERN _XXX_
        for x, y in stone_list[player]:
            # Check column
            if (hasStonePatternInList(stone_list[player], [(x + 1, y), (x + 2, y)])
                and (x - 1, y) in free_spots and (x + 3, y) in free_spots):
                count += 1
            # Check line
            if (hasStonePatternInList(stone_list[player], [(x, y + 1), (x, y + 2)])
                and (x, y - 1) in free_spots and (x, y + 3) in free_spots):
                count += 1
            # Check left diagonal
            if (hasStonePatternInList(stone_list[player], [(x + 1, y + 1), (x + 2, y + 2)])
                and (x - 1, y - 1) in free_spots and (x + 3, y + 3) in free_spots):
                count += 1
        # Check right diagonal
            if (hasStonePatternInList(stone_list[player], [(x - 1, y + 1), (x - 2, y + 2)])
                and (x + 1, y - 1) in free_spots and (x - 3, y + 3) in free_spots):
                count += 1

        ### PATTERN X_XX
        for x, y in stone_list[player]:
            # Check column
            if (hasStonePatternInList(stone_list[player], [(x + 2, y), (x + 3, y)])
                and (x + 1, y) in free_spots):
                count += 1
            # Check line
            if (hasStonePatternInList(stone_list[player], [(x, y + 2), (x, y + 3)])
                and (x, y + 1) in free_spots):
                count += 1
            # Check left diagonal
            if (hasStonePatternInList(stone_list[player], [(x + 2, y + 2), (x + 3, y + 3)])
                and (x + 1, y + 1) in free_spots):
                count += 1
        # Check right diagonal
            if (hasStonePatternInList(stone_list[player], [(x - 2, y + 2), (x - 3, y + 3)])
                and (x - 1, y + 1) in free_spots):
                count += 1

        ### PATTERN XX_X
        for x, y in stone_list[player]:
            # Check column
            if (hasStonePatternInList(stone_list[player], [(x + 1, y), (x + 3, y)])
                and (x + 2, y) in free_spots):
                count += 1
            # Check line
            if (hasStonePatternInList(stone_list[player], [(x, y + 1), (x, y + 3)])
                and (x, y + 2) in free_spots):
                count += 1
            # Check left diagonal
            if (hasStonePatternInList(stone_list[player], [(x + 1, y + 1), (x + 3, y + 3)])
                and (x + 2, y + 2) in free_spots):
                count += 1
        # Check right diagonal
            if (hasStonePatternInList(stone_list[player], [(x - 1, y + 1), (x - 3, y + 3)])
                and (x - 2, y + 2) in free_spots):
                count += 1

        ### PATTERN XX__X
        for x, y in stone_list[player]:
            # Check column
            if (hasStonePatternInList(stone_list[player], [(x + 1, y), (x + 4, y)])
                and (x + 2, y) in free_spots and (x + 3, y) in free_spots):
                count += 1
            # Check line
            if (hasStonePatternInList(stone_list[player], [(x, y + 1), (x, y + 4)])
                and (x, y + 2) in free_spots and (x, y + 3) in free_spots):
                count += 1
            # Check left diagonal
            if (hasStonePatternInList(stone_list[player], [(x + 1, y + 1), (x + 4, y + 4)])
                and (x + 2, y + 2) in free_spots and (x + 3, y + 3) in free_spots):
                count += 1
            # Check right diagonal
            if (hasStonePatternInList(stone_list[player], [(x - 1, y + 1), (x - 4, y + 4)])
                and (x - 2, y + 2) in free_spots and (x - 3, y + 3) in free_spots):
                count += 1

        ### PATTERN X__XX
        for x, y in stone_list[player]:
            # Check column
            if (hasStonePatternInList(stone_list[player], [(x + 3, y), (x + 4, y)])
                and (x + 1, y) in free_spots and (x + 2, y) in free_spots):
                count += 1
            # Check line
            if (hasStonePatternInList(stone_list[player], [(x, y + 3), (x, y + 4)])
                and (x, y + 1) in free_spots and (x, y + 2) in free_spots):
                count += 1
            # Check left diagonal
            if (hasStonePatternInList(stone_list[player], [(x + 3, y + 3), (x + 4, y + 4)])
                and (x + 1, y + 1) in free_spots and (x + 2, y + 2) in free_spots):
                count += 1
            # Check right diagonal
            if (hasStonePatternInList(stone_list[player], [(x - 3, y + 3), (x - 4, y + 4)])
                and (x - 1, y + 1) in free_spots and (x - 2, y + 2) in free_spots):
                count += 1

        ### PATTERN X_X_X
        for x, y in stone_list[player]:
            # Check column
            if (hasStonePatternInList(stone_list[player], [(x + 2, y), (x + 4, y)])
                and (x + 1, y) in free_spots and (x + 3, y) in free_spots):
                count += 1
            # Check line
            if (hasStonePatternInList(stone_list[player], [(x, y + 2), (x, y + 4)])
                and (x, y + 1) in free_spots and (x, y + 3) in free_spots):
                count += 1
            # Check left diagonal
            if (hasStonePatternInList(stone_list[player], [(x + 2, y + 2), (x + 4, y + 4)])
                and (x + 1, y + 1) in free_spots and (x + 3, y + 3) in free_spots):
                count += 1
            # Check right diagonal
            if (hasStonePatternInList(stone_list[player], [(x - 2, y + 2), (x - 4, y + 4)])
                and (x - 1, y + 1) in free_spots and (x - 3, y + 3) in free_spots):
                count += 1
        return count

    @staticmethod
    def hasDeadThree(stone_list, player, opponent, possible_moves, forbidden_move):
        free_spots = possible_moves - forbidden_move[player]
        free_spots_and_player_stones = free_spots | stone_list[player]
        count = 0
        ### CHECK PATTERN OXXX_
        for x, y in stone_list[player]:
            # Check column
            if (hasStonePatternInList(stone_list[player], [(x + 1, y), (x + 2, y)])
                and (((x - 1, y) in free_spots) ^ ((x + 3, y) in free_spots))
                and (((x - 1, y) not in free_spots_and_player_stones) ^ ((x + 3, y) not in free_spots_and_player_stones))):
                count += 1
            # Check line
            if (hasStonePatternInList(stone_list[player], [(x, y + 1), (x, y + 2)])
                and (((x, y - 1) in free_spots) ^ ((x, y + 3) in free_spots))
                and (((x, y - 1) not in free_spots_and_player_stones) ^ ((x, y + 3) not in free_spots_and_player_stones))):
                count += 1
            # Check left diagonal
            if (hasStonePatternInList(stone_list[player], [(x + 1, y + 1), (x + 2, y + 2)])
                and (((x - 1, y - 1) in free_spots) ^ ((x + 3, y + 3) in free_spots))
                and (((x - 1, y - 1) not in free_spots_and_player_stones) ^ ((x + 3, y + 3) not in free_spots_and_player_stones))):
                count += 1
            # Check right diagonal
            if (hasStonePatternInList(stone_list[player], [(x - 1, y + 1), (x - 2, y + 2)])
                and (((x + 1, y - 1) in free_spots) ^ ((x - 3, y + 3) in free_spots))
                and (((x + 1, y - 1) not in free_spots_and_player_stones) ^ ((x - 3, y + 3) not in free_spots_and_player_stones))):
                count += 1

        ### CHECK PATTERN OXX_X        TODO =>         X_XXO
        for x, y in stone_list[player]:
            # Check column
            if (hasStonePatternInList(stone_list[player], [(x + 1, y), (x + 3, y)])
                and (((x - 1, y) not in free_spots_and_player_stones) and ((x + 2, y) in free_spots))):
                and (((x + 1, y - 1) in free_spots) ^ ((x - 3, y + 3) in free_spots))
                and (((x + 1, y - 1) not in free_spots_and_player_stones) ^ ((x - 3, y + 3) not in free_spots_and_player_stones))):
                count += 1
            # Check line
            if (hasStonePatternInList(stone_list[player], [(x, y + 1), (x, y + 3)])
                and (((x, y - 1) not in free_spots_and_player_stones) and ((x, y + 2) in free_spots))):
                and (((x + 1, y - 1) in free_spots) ^ ((x - 3, y + 3) in free_spots))
                and (((x + 1, y - 1) not in free_spots_and_player_stones) ^ ((x - 3, y + 3) not in free_spots_and_player_stones))):
                count += 1
            # Check left diagonal
            if (hasStonePatternInList(stone_list[player], [(x + 1, y + 1), (x + 3, y + 3)])
                and (((x - 1, y - 1) not in free_spots_and_player_stones) and ((x + 2, y + 2) in free_spots))):
                and (((x + 1, y - 1) in free_spots) ^ ((x - 3, y + 3) in free_spots))
                and (((x + 1, y - 1) not in free_spots_and_player_stones) ^ ((x - 3, y + 3) not in free_spots_and_player_stones))):
                count += 1
            # Check right diagonal
            if (hasStonePatternInList(stone_list[player], [(x - 1, y + 1), (x - 3, y + 3)])
                and (((x + 1, y - 1) not in free_spots_and_player_stones) and ((x - 2, y + 2) in free_spots))):
                and (((x + 1, y - 1) in free_spots) ^ ((x - 3, y + 3) in free_spots))
                and (((x + 1, y - 1) not in free_spots_and_player_stones) ^ ((x - 3, y + 3) not in free_spots_and_player_stones))):
                count += 1


        return count