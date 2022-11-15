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
        while i <= 4 and CheckRules._checkCondition(x - i, y, stone_list, player, goban_size):
            count += 1
            i += 1
        i = 1
        while i <= 4 and CheckRules._checkCondition(x + i, y, stone_list, player, goban_size):
            count += 1
            i += 1
        if count >= 5:
            return True
        return False
 
    @staticmethod   
    def _hasColumn(x, y, stone_list, player, goban_size):
        i = 1
        count = 1
        while i <= 4 and CheckRules._checkCondition(x, y - i, stone_list, player, goban_size):
            count += 1
            i += 1
        i = 1
        while i <= 4 and CheckRules._checkCondition(x, y + i, stone_list, player, goban_size):
            count += 1
            i += 1
        if count >= 5:
            return True
        return False

    @staticmethod
    def _hasLeftDiagonal(x, y, stone_list, player, goban_size):
        i = 1
        count = 1
        while i <= 4 and CheckRules._checkCondition(x - i, y - i, stone_list, player, goban_size):
            count += 1
            i += 1
        i = 1
        while i <= 4 and CheckRules._checkCondition(x + i, y + i, stone_list, player, goban_size):
            count += 1
            i += 1
        if count >= 5:
            return True
        return False

    @staticmethod
    def _hasRightDiagonal(x, y, stone_list, player, goban_size):
        i = 1
        count = 1
        while i <= 4 and CheckRules._checkCondition(x + i, y - i, stone_list, player, goban_size):
            count += 1
            i += 1
        i = 1
        while i <= 4 and CheckRules._checkCondition(x - i, y + i, stone_list, player, goban_size):
            count += 1
            i += 1
        if count >= 5:
            return True
        return False

##############################################################################################################
    @staticmethod
    def _checkThreeCondition(x, y, stone_list, player, goban_size):
        # print((x, y) in stone_list[player], x >= 0 and x < goban_size, y >= 0 and y < goban_size)
        return (x >= 0 and x < goban_size
                and y >= 0 and y < goban_size)

    @staticmethod
    def _hasLineThree(x, y, stone_list, player, goban_size):
        i = 1
        count = 1
        while i <= 3 and CheckRules._checkThreeCondition(x - i, y, stone_list, player, goban_size):
            if (x - i, y) in stone_list[player]:
                count += 1
            i += 1
        i = 1
        while i <= 3 and CheckRules._checkThreeCondition(x + i, y, stone_list, player, goban_size):
            if (x + i, y) in stone_list[player]:
                count += 1
            i += 1
        if count == 3:
            return True
        return False
    
    @staticmethod
    def _hasColumnThree(x, y, stone_list, player, goban_size):
        i = 1
        count = 1
        while i <= 3 and CheckRules._checkThreeCondition(x, y - i, stone_list, player, goban_size):
            if (x, y - i) in stone_list[player]:
                count += 1
            i += 1
        i = 1
        while i <= 3 and CheckRules._checkThreeCondition(x, y + i, stone_list, player, goban_size):
            if (x, y + i) in stone_list[player]:
                count += 1
            i += 1
        if count == 3:
            return True
        return False
    
    @staticmethod
    def _hasLeftDiagonalThree(x, y, stone_list, player, goban_size):
        i = 1
        count = 1
        while i <= 3 and CheckRules._checkThreeCondition(x - i, y - i, stone_list, player, goban_size):
            if (x - i, y - i) in stone_list[player]:
                count += 1
            i += 1
        i = 1
        while i <= 3 and CheckRules._checkThreeCondition(x + i, y + i, stone_list, player, goban_size):
            if (x + i, y + i) in stone_list[player]:
                count += 1
            i += 1
        if count == 3:
            return True
        return False

    @staticmethod
    def _hasRightDiagonalThree(x, y, stone_list, player, goban_size):
        i = 1
        count = 1
        while i <= 3 and CheckRules._checkThreeCondition(x + i, y - i, stone_list, player, goban_size):
            if (x + i, y - i) in stone_list[player]:
                count += 1
            i += 1
        i = 1
        while i <= 3 and CheckRules._checkThreeCondition(x - i, y + i, stone_list, player, goban_size):
            if (x - i, y + i) in stone_list[player]:
                count += 1
            i += 1
        if count == 3:
            return True
        return False