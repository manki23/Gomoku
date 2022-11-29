class CheckRules():
    @staticmethod
    def _checkCondition(x, y, stone_list, player, goban_size):
        return ((x, y) in stone_list[player]
                and x >= 0 and x < goban_size
                and y >= 0 and y < goban_size)

    @staticmethod
    def _hasLine(x, y, stone_list, player, goban_size):
        i = 1
        count = 1
        res = {(x, y)}
        while i <= 4 and CheckRules._checkCondition(x - i, y, stone_list, player, goban_size):
            count += 1
            res.add((x - i, y))
            i += 1
        i = 1
        while i <= 4 and CheckRules._checkCondition(x + i, y, stone_list, player, goban_size):
            count += 1
            res.add((x + i, y))
            i += 1
        if count >= 5:
            return res
        return set()
 
    @staticmethod   
    def _hasColumn(x, y, stone_list, player, goban_size):
        i = 1
        count = 1
        res = {(x, y)}
        while i <= 4 and CheckRules._checkCondition(x, y - i, stone_list, player, goban_size):
            count += 1
            res.add((x, y - i))
            i += 1
        i = 1
        while i <= 4 and CheckRules._checkCondition(x, y + i, stone_list, player, goban_size):
            count += 1
            res.add((x, y + i))
            i += 1
        if count >= 5:
            return res
        return set()

    @staticmethod
    def _hasLeftDiagonal(x, y, stone_list, player, goban_size):
        i = 1
        count = 1
        res = {(x, y)}
        while i <= 4 and CheckRules._checkCondition(x - i, y - i, stone_list, player, goban_size):
            count += 1
            res.add((x - i, y - i))
            i += 1
        i = 1
        while i <= 4 and CheckRules._checkCondition(x + i, y + i, stone_list, player, goban_size):
            count += 1
            res.add((x + i, y + i))
            i += 1
        if count >= 5:
            return res
        return set()

    @staticmethod
    def _hasRightDiagonal(x, y, stone_list, player, goban_size):
        i = 1
        count = 1
        res = {(x, y)}
        while i <= 4 and CheckRules._checkCondition(x + i, y - i, stone_list, player, goban_size):
            count += 1
            res.add((x + i, y - i))
            i += 1
        i = 1
        while i <= 4 and CheckRules._checkCondition(x - i, y + i, stone_list, player, goban_size):
            count += 1
            res.add((x - i, y + i))
            i += 1
        if count >= 5:
            return res
        return set()


##############################################################################################################

    @staticmethod
    def _getCaptures(x, y, stone_list, player, opponent):
        res = set()
        if (x + 1, y) in stone_list[opponent] and (x + 2, y) in stone_list[opponent] and (x + 3, y) in stone_list[player]:
            res |= {(x + 1, y), (x + 2, y)}
        if (x - 1, y) in stone_list[opponent] and (x - 2, y) in stone_list[opponent] and (x - 3, y) in stone_list[player]:
            res |= {(x - 1, y), (x - 2, y)}
        if (x, y + 1) in stone_list[opponent] and (x, y + 2) in stone_list[opponent] and (x, y + 3) in stone_list[player]:
            res |= {(x, y + 1), (x, y + 2)}
        if (x, y - 1) in stone_list[opponent] and (x, y - 2) in stone_list[opponent] and (x, y - 3) in stone_list[player]:
            res |= {(x, y - 1), (x, y - 2)}
        if (x - 1, y - 1) in stone_list[opponent] and (x - 2, y - 2) in stone_list[opponent] and (x - 3, y - 3) in stone_list[player]:
            res |= {(x - 1, y - 1), (x - 2, y - 2)}
        if (x + 1, y + 1) in stone_list[opponent] and (x + 2, y + 2) in stone_list[opponent] and (x + 3, y + 3) in stone_list[player]:
            res |= {(x + 1, y + 1), (x + 2, y + 2)}
        if (x - 1, y + 1) in stone_list[opponent] and (x - 2, y + 2) in stone_list[opponent] and (x - 3, y + 3) in stone_list[player]:
            res |= {(x - 1, y + 1), (x - 2, y + 2)}
        if (x + 1, y - 1) in stone_list[opponent] and (x + 2, y - 2) in stone_list[opponent] and (x + 3, y - 3) in stone_list[player]:
            res |= {(x + 1, y - 1), (x + 2, y - 2)}
        return res

    @staticmethod
    def _getOpponentCaptures(x, y, stone_list, player, opponent, possible_moves, forbidden_move):
        res = set()
        # all_stones = stone_list[player] | stone_list[opponent]
        op_free_spots = possible_moves - forbidden_move[opponent]

        if (x - 1, y) in stone_list[opponent] and (x + 1, y) in stone_list[player] and (x + 2, y) in op_free_spots:
            return True
        if (x + 1, y) in stone_list[opponent] and (x - 1, y) in stone_list[player] and (x - 2, y) in op_free_spots:
            return True
        if (x, y + 1) in stone_list[opponent] and (x, y - 1) in stone_list[player] and (x, y - 2) in op_free_spots:
            return True
        if (x, y - 1) in stone_list[opponent] and (x, y + 1) in stone_list[player] and (x, y + 2) in op_free_spots:
            return True
        if (x - 1, y - 1) in stone_list[opponent] and (x + 1, y + 1) in stone_list[player] and (x + 2, y + 2) in op_free_spots:
            return True
        if (x + 1, y + 1) in stone_list[opponent] and (x - 1, y - 1) in stone_list[player] and (x - 2, y - 2) in op_free_spots:
            return True
        if (x - 1, y + 1) in stone_list[opponent] and (x + 1, y - 1) in stone_list[player] and (x + 2, y - 2) in op_free_spots:
            return True
        if (x + 1, y - 1) in stone_list[opponent] and (x - 1, y + 1) in stone_list[player] and (x - 2, y + 2) in op_free_spots:
            return True
        return False

##############################################################################################################

    @staticmethod
    def _hasVerticalFreeThree(x, y, stone_list, player, possible_moves):
        ######################### Pattern X000X
        if ((x, y + 1) in stone_list[player]
            and (x, y + 2) in stone_list[player]
            and (x, y + 3) in possible_moves
            and (x, y - 1) in possible_moves):
            return True

        if ((x, y - 1) in stone_list[player]
            and (x, y - 2) in stone_list[player]
            and (x, y - 3) in possible_moves
            and (x, y + 1) in possible_moves):
            return True

        if ((x, y - 1) in stone_list[player]
            and (x, y + 1) in stone_list[player]
            and (x, y + 2) in possible_moves
            and (x, y - 2) in possible_moves):
            return True                   

        ######################## Pattern X00X0X
        if ((x, y - 1) in stone_list[player]
            and (x, y - 3) in stone_list[player]
            and (x, y - 2) in possible_moves
            and (x, y - 4) in possible_moves
            and (x, y + 1) in possible_moves):
            return True

        if ((x, y + 1) in stone_list[player]
            and (x, y - 2) in stone_list[player]
            and (x, y + 2) in possible_moves
            and (x, y - 3) in possible_moves
            and (x, y - 1) in possible_moves):
            return True
        
        if ((x, y + 2) in stone_list[player]
            and (x, y + 3) in stone_list[player]
            and (x, y + 1) in possible_moves
            and (x, y + 4) in possible_moves
            and (x, y - 1) in possible_moves):
            return True

        ######################### Pattern X0X00X
        if ((x, y + 1) in stone_list[player]
            and (x, y + 3) in stone_list[player]
            and (x, y + 2) in possible_moves
            and (x, y + 4) in possible_moves
            and (x, y - 1) in possible_moves):
            return True

        if ((x, y - 1) in stone_list[player]
            and (x, y + 2) in stone_list[player]
            and (x, y + 1) in possible_moves
            and (x, y - 2) in possible_moves
            and (x, y + 3) in possible_moves):
            return True

        if ((x, y - 2) in stone_list[player]
            and (x, y - 3) in stone_list[player]
            and (x, y + 1) in possible_moves
            and (x, y - 1) in possible_moves
            and (x, y - 4) in possible_moves):
            return True
        return False

    @staticmethod
    def _hasHorizontalFreeThree(x, y, stone_list, player, possible_moves):
        ######################### Pattern X000X
        if ((x + 1, y) in stone_list[player]
            and (x + 2, y) in stone_list[player]
            and (x + 2, y) in possible_moves
            and (x - 1, y) in possible_moves):
            return True

        if ((x - 1, y) in stone_list[player]
            and (x - 2 , y) in stone_list[player]
            and (x - 3, y) in possible_moves
            and (x + 1, y) in possible_moves):
            return True

        if ((x - 1, y) in stone_list[player]
            and (x + 1, y) in stone_list[player]
            and (x + 2, y) in possible_moves
            and (x - 2, y) in possible_moves):
            return True

        ######################## Pattern X00X0X
        if ((x - 1, y) in stone_list[player]
            and (x - 3, y) in stone_list[player]
            and (x - 2, y) in possible_moves
            and (x - 4, y) in possible_moves
            and (x + 1, y) in possible_moves):
            return True

        if ((x + 1, y) in stone_list[player]
            and (x - 2, y) in stone_list[player]
            and (x + 2, y) in possible_moves
            and (x - 3, y) in possible_moves
            and (x - 1, y) in possible_moves):
            return True
        
        if ((x + 2, y) in stone_list[player]
            and (x + 3, y) in stone_list[player]
            and (x + 1, y) in possible_moves
            and (x + 4, y) in possible_moves
            and (x - 1, y) in possible_moves):
            return True

        ######################### Pattern X0X00X
        if ((x + 1, y) in stone_list[player]
            and (x + 3, y) in stone_list[player]
            and (x + 2, y) in possible_moves
            and (x + 4, y) in possible_moves
            and (x - 1, y) in possible_moves):
            return True

        if ((x - 1, y) in stone_list[player]
            and (x + 2, y) in stone_list[player]
            and (x + 1, y) in possible_moves
            and (x - 2, y) in possible_moves
            and (x + 3, y) in possible_moves):
            return True

        if ((x - 2, y) in stone_list[player]
            and (x - 3, y) in stone_list[player]
            and (x + 1, y) in possible_moves
            and (x - 1, y) in possible_moves
            and (x - 4, y) in possible_moves):
            return True
        return False

    @staticmethod
    def _hasLeftDiagonalFreeThree(x, y, stone_list, player, possible_moves):
        ######################### Pattern X000X
        if ((x + 1, y + 1) in stone_list[player]
            and (x + 2, y + 2) in stone_list[player]
            and (x + 3, y + 3) in possible_moves
            and (x - 1, y - 1) in possible_moves):
            return True

        if ((x - 1, y - 1) in stone_list[player]
            and (x - 2, y - 2) in stone_list[player]
            and (x - 3, y - 3) in possible_moves
            and (x + 1, y + 1) in possible_moves):
            return True

        if ((x - 1, y - 1) in stone_list[player]
            and (x + 1, y + 1) in stone_list[player]
            and (x + 2, y + 2) in possible_moves
            and (x - 2, y - 2) in possible_moves):
            return True

        ######################## Pattern X00X0X
        if ((x - 1, y - 1) in stone_list[player]
            and (x - 3, y - 3) in stone_list[player]
            and (x - 2, y - 2) in possible_moves
            and (x - 4, y - 4) in possible_moves
            and (x + 1, y + 1) in possible_moves):
            return True

        if ((x + 1, y + 1) in stone_list[player]
            and (x - 2, y - 2) in stone_list[player]
            and (x + 2, y + 2) in possible_moves
            and (x - 3, y - 3) in possible_moves
            and (x - 1, y - 1) in possible_moves):
            return True
        
        if ((x + 2, y + 2) in stone_list[player]
            and (x + 3, y + 3) in stone_list[player]
            and (x + 1, y + 1) in possible_moves
            and (x + 4, y + 4) in possible_moves
            and (x - 1, y - 1) in possible_moves):
            return True

        ######################### Pattern X0X00X
        if ((x + 1, y + 1) in stone_list[player]
            and (x + 3, y + 3) in stone_list[player]
            and (x + 2, y + 2) in possible_moves
            and (x + 4, y + 4) in possible_moves
            and (x - 1, y - 1) in possible_moves):
            return True

        if ((x - 1, y - 1) in stone_list[player]
            and (x + 2, y + 2) in stone_list[player]
            and (x + 1, y + 1) in possible_moves
            and (x - 2, y - 2) in possible_moves
            and (x + 3, y + 3) in possible_moves):
            return True

        if ((x - 2, y - 2) in stone_list[player]
            and (x - 3, y - 3) in stone_list[player]
            and (x + 1, y + 1) in possible_moves
            and (x - 1, y - 1) in possible_moves
            and (x - 4, y - 4) in possible_moves):
            return True
        return False

    @staticmethod
    def _hasRightDiagonalFreeThree(x, y, stone_list, player, possible_moves):
        ######################### Pattern X000X
        if ((x - 1, y + 1) in stone_list[player]
            and (x - 2, y + 2) in stone_list[player]
            and (x - 3, y + 3) in possible_moves
            and (x + 1, y - 1) in possible_moves):
            return True

        if ((x + 1, y - 1) in stone_list[player]
            and (x + 2, y - 2) in stone_list[player]
            and (x + 3, y - 3) in possible_moves
            and (x - 1, y + 1) in possible_moves):
            return True

        if ((x + 1, y - 1) in stone_list[player]
            and (x - 1, y + 1) in stone_list[player]
            and (x - 2, y + 2) in possible_moves
            and (x + 2, y - 2) in possible_moves):
            return True

        ######################## Pattern X00X0X
        if ((x + 1, y - 1) in stone_list[player]
            and (x + 3, y - 3) in stone_list[player]
            and (x + 2, y - 2) in possible_moves
            and (x + 4, y - 4) in possible_moves
            and (x - 1, y + 1) in possible_moves):
            return True

        if ((x - 1, y + 1) in stone_list[player]
            and (x + 2, y - 2) in stone_list[player]
            and (x - 2, y + 2) in possible_moves
            and (x + 3, y - 3) in possible_moves
            and (x + 1, y - 1) in possible_moves):
            return True
        
        if ((x - 2, y + 2) in stone_list[player]
            and (x - 3, y + 3) in stone_list[player]
            and (x - 1, y + 1) in possible_moves
            and (x - 4, y + 4) in possible_moves
            and (x + 1, y - 1) in possible_moves):
            return True

        ######################### Pattern X0X00X
        if ((x - 1, y + 1) in stone_list[player]
            and (x - 3, y + 3) in stone_list[player]
            and (x - 2, y + 2) in possible_moves
            and (x - 4, y + 4) in possible_moves
            and (x + 1, y - 1) in possible_moves):
            return True

        if ((x + 1, y - 1) in stone_list[player]
            and (x - 2, y + 2) in stone_list[player]
            and (x - 1, y + 1) in possible_moves
            and (x + 2, y - 2) in possible_moves
            and (x - 3, y + 3) in possible_moves):
            return True

        if ((x + 2, y - 2) in stone_list[player]
            and (x + 3, y - 3) in stone_list[player]
            and (x - 1, y + 1) in possible_moves
            and (x + 1, y - 1) in possible_moves
            and (x + 4, y - 4) in possible_moves):
            return True
        return False