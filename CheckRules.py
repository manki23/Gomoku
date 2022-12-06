class CheckRules():
    @staticmethod
    def _checkCondition(x, y, game):
        return ((x, y) in game.stone_list[game.player]
                and 0 <= x < game.goban_size
                and 0 <= y < game.goban_size)

    @staticmethod
    def hasLine(x, y, game):
        i = 1
        count = 1
        res = {(x, y)}
        while i <= 4 and CheckRules._checkCondition(x - i, y, game):
            count += 1
            res.add((x - i, y))
            i += 1
        i = 1
        while i <= 4 and CheckRules._checkCondition(x + i, y, game):
            count += 1
            res.add((x + i, y))
            i += 1
        if count >= 5:
            return res
        return set()
 
    @staticmethod   
    def hasColumn(x, y, game):
        i = 1
        count = 1
        res = {(x, y)}
        while i <= 4 and CheckRules._checkCondition(x, y - i, game):
            count += 1
            res.add((x, y - i))
            i += 1
        i = 1
        while i <= 4 and CheckRules._checkCondition(x, y + i, game):
            count += 1
            res.add((x, y + i))
            i += 1
        if count >= 5:
            return res
        return set()

    @staticmethod
    def hasLeftDiagonal(x, y, game):
        i = 1
        count = 1
        res = {(x, y)}
        while i <= 4 and CheckRules._checkCondition(x - i, y - i, game):
            count += 1
            res.add((x - i, y - i))
            i += 1
        i = 1
        while i <= 4 and CheckRules._checkCondition(x + i, y + i, game):
            count += 1
            res.add((x + i, y + i))
            i += 1
        if count >= 5:
            return res
        return set()

    @staticmethod
    def hasRightDiagonal(x, y, game):
        i = 1
        count = 1
        res = {(x, y)}
        while i <= 4 and CheckRules._checkCondition(x + i, y - i, game):
            count += 1
            res.add((x + i, y - i))
            i += 1
        i = 1
        while i <= 4 and CheckRules._checkCondition(x - i, y + i, game):
            count += 1
            res.add((x - i, y + i))
            i += 1
        if count >= 5:
            return res
        return set()


##############################################################################################################

    @staticmethod
    def getCaptures(x, y, game, player, opponent):
        res = set()
        stone_list = game.stone_list
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
    def wasCaptures(x, y, game, player, captures):
        res = set()
        stone_list = game.stone_list
        if (x + 1, y) in captures and (x + 2, y) in captures and (x + 3, y) in stone_list[player]:
            res |= {(x + 1, y), (x + 2, y)}
        if (x - 1, y) in captures and (x - 2, y) in captures and (x - 3, y) in stone_list[player]:
            res |= {(x - 1, y), (x - 2, y)}
        if (x, y + 1) in captures and (x, y + 2) in captures and (x, y + 3) in stone_list[player]:
            res |= {(x, y + 1), (x, y + 2)}
        if (x, y - 1) in captures and (x, y - 2) in captures and (x, y - 3) in stone_list[player]:
            res |= {(x, y - 1), (x, y - 2)}
        if (x - 1, y - 1) in captures and (x - 2, y - 2) in captures and (x - 3, y - 3) in stone_list[player]:
            res |= {(x - 1, y - 1), (x - 2, y - 2)}
        if (x + 1, y + 1) in captures and (x + 2, y + 2) in captures and (x + 3, y + 3) in stone_list[player]:
            res |= {(x + 1, y + 1), (x + 2, y + 2)}
        if (x - 1, y + 1) in captures and (x - 2, y + 2) in captures and (x - 3, y + 3) in stone_list[player]:
            res |= {(x - 1, y + 1), (x - 2, y + 2)}
        if (x + 1, y - 1) in captures and (x + 2, y - 2) in captures and (x + 3, y - 3) in stone_list[player]:
            res |= {(x + 1, y - 1), (x + 2, y - 2)}
        return res

    @staticmethod
    def getOpponentCaptures(x, y, game):
        res = set()
        op_free_spots = game.possible_moves - game.forbidden_moves[game.opponent]
        stone_list = game.stone_list

        if (
            (((x - 1, y) in stone_list[game.opponent] and (x + 2, y) in op_free_spots) or 
            ((x + 2, y) in stone_list[game.opponent] and (x - 1, y) in op_free_spots))
            and (x + 1, y) in stone_list[game.player] ):
            return True
        if (
            (((x + 1, y) in stone_list[game.opponent] and (x - 2, y) in op_free_spots) or
            ((x - 2, y) in stone_list[game.opponent] and (x + 1, y) in op_free_spots))
            and (x - 1, y) in stone_list[game.player]):
            return True           
        if (
            (((x, y + 1) in stone_list[game.opponent] and (x, y - 2) in op_free_spots) or
            ((x, y - 2) in stone_list[game.opponent] and (x, y + 1) in op_free_spots)) 
            and (x, y - 1) in stone_list[game.player]):
            return True
        if (
            (((x, y - 1) in stone_list[game.opponent] and (x, y + 2) in op_free_spots) or
            ((x, y + 2) in stone_list[game.opponent] and (x, y - 1) in op_free_spots))
            and (x, y + 1) in stone_list[game.player]):
            return True
        if (
            (((x - 1, y - 1) in stone_list[game.opponent] and (x + 2, y + 2) in op_free_spots) or
            ((x + 2, y + 2) in stone_list[game.opponent] and (x - 1, y - 1) in op_free_spots))
            and (x + 1, y + 1) in stone_list[game.player]):
            return True
        if (
            (((x + 1, y + 1) in stone_list[game.opponent] and (x - 2, y - 2) in op_free_spots) or
            ((x - 2, y - 2) in stone_list[game.opponent] and (x + 1, y + 1) in op_free_spots))
            and (x - 1, y - 1) in stone_list[game.player]):
            return True
        if (
            (((x - 1, y + 1) in stone_list[game.opponent] and (x + 2, y - 2) in op_free_spots) or
            ((x + 2, y - 2) in stone_list[game.opponent] and (x - 1, y + 1) in op_free_spots))
            and (x + 1, y - 1) in stone_list[game.player]):
            return True
        if (
            (((x + 1, y - 1) in stone_list[game.opponent] and (x - 2, y + 2) in op_free_spots) or
            ((x - 2, y + 2) in stone_list[game.opponent] and (x + 1, y - 1) in op_free_spots))
            and (x - 1, y + 1) in stone_list[game.player]):
            return True
        return False

##############################################################################################################

    @staticmethod
    def hasVerticalFreeThree(x, y, game, player):
        ######################### Pattern X000X
        if ((x, y + 1) in game.stone_list[player]
            and (x, y + 2) in game.stone_list[player]
            and (x, y + 3) in game.possible_moves
            and (x, y - 1) in game.possible_moves):
            return True

        if ((x, y - 1) in game.stone_list[player]
            and (x, y - 2) in game.stone_list[player]
            and (x, y - 3) in game.possible_moves
            and (x, y + 1) in game.possible_moves):
            return True

        if ((x, y - 1) in game.stone_list[player]
            and (x, y + 1) in game.stone_list[player]
            and (x, y + 2) in game.possible_moves
            and (x, y - 2) in game.possible_moves):
            return True                   

        ######################## Pattern X00X0X
        if ((x, y - 1) in game.stone_list[player]
            and (x, y - 3) in game.stone_list[player]
            and (x, y - 2) in game.possible_moves
            and (x, y - 4) in game.possible_moves
            and (x, y + 1) in game.possible_moves):
            return True

        if ((x, y + 1) in game.stone_list[player]
            and (x, y - 2) in game.stone_list[player]
            and (x, y + 2) in game.possible_moves
            and (x, y - 3) in game.possible_moves
            and (x, y - 1) in game.possible_moves):
            return True
        
        if ((x, y + 2) in game.stone_list[player]
            and (x, y + 3) in game.stone_list[player]
            and (x, y + 1) in game.possible_moves
            and (x, y + 4) in game.possible_moves
            and (x, y - 1) in game.possible_moves):
            return True

        ######################### Pattern X0X00X
        if ((x, y + 1) in game.stone_list[player]
            and (x, y + 3) in game.stone_list[player]
            and (x, y + 2) in game.possible_moves
            and (x, y + 4) in game.possible_moves
            and (x, y - 1) in game.possible_moves):
            return True

        if ((x, y - 1) in game.stone_list[player]
            and (x, y + 2) in game.stone_list[player]
            and (x, y + 1) in game.possible_moves
            and (x, y - 2) in game.possible_moves
            and (x, y + 3) in game.possible_moves):
            return True

        if ((x, y - 2) in game.stone_list[player]
            and (x, y - 3) in game.stone_list[player]
            and (x, y + 1) in game.possible_moves
            and (x, y - 1) in game.possible_moves
            and (x, y - 4) in game.possible_moves):
            return True
        return False

    @staticmethod
    def hasHorizontalFreeThree(x, y, game, player):
        ######################### Pattern X000X
        if ((x + 1, y) in game.stone_list[player]
            and (x + 2, y) in game.stone_list[player]
            and (x + 2, y) in game.possible_moves
            and (x - 1, y) in game.possible_moves):
            return True

        if ((x - 1, y) in game.stone_list[player]
            and (x - 2 , y) in game.stone_list[player]
            and (x - 3, y) in game.possible_moves
            and (x + 1, y) in game.possible_moves):
            return True

        if ((x - 1, y) in game.stone_list[player]
            and (x + 1, y) in game.stone_list[player]
            and (x + 2, y) in game.possible_moves
            and (x - 2, y) in game.possible_moves):
            return True

        ######################## Pattern X00X0X
        if ((x - 1, y) in game.stone_list[player]
            and (x - 3, y) in game.stone_list[player]
            and (x - 2, y) in game.possible_moves
            and (x - 4, y) in game.possible_moves
            and (x + 1, y) in game.possible_moves):
            return True

        if ((x + 1, y) in game.stone_list[player]
            and (x - 2, y) in game.stone_list[player]
            and (x + 2, y) in game.possible_moves
            and (x - 3, y) in game.possible_moves
            and (x - 1, y) in game.possible_moves):
            return True
        
        if ((x + 2, y) in game.stone_list[player]
            and (x + 3, y) in game.stone_list[player]
            and (x + 1, y) in game.possible_moves
            and (x + 4, y) in game.possible_moves
            and (x - 1, y) in game.possible_moves):
            return True

        ######################### Pattern X0X00X
        if ((x + 1, y) in game.stone_list[player]
            and (x + 3, y) in game.stone_list[player]
            and (x + 2, y) in game.possible_moves
            and (x + 4, y) in game.possible_moves
            and (x - 1, y) in game.possible_moves):
            return True

        if ((x - 1, y) in game.stone_list[player]
            and (x + 2, y) in game.stone_list[player]
            and (x + 1, y) in game.possible_moves
            and (x - 2, y) in game.possible_moves
            and (x + 3, y) in game.possible_moves):
            return True

        if ((x - 2, y) in game.stone_list[player]
            and (x - 3, y) in game.stone_list[player]
            and (x + 1, y) in game.possible_moves
            and (x - 1, y) in game.possible_moves
            and (x - 4, y) in game.possible_moves):
            return True
        return False

    @staticmethod
    def hasLeftDiagonalFreeThree(x, y, game, player):
        ######################### Pattern X000X
        if ((x + 1, y + 1) in game.stone_list[player]
            and (x + 2, y + 2) in game.stone_list[player]
            and (x + 3, y + 3) in game.possible_moves
            and (x - 1, y - 1) in game.possible_moves):
            return True

        if ((x - 1, y - 1) in game.stone_list[player]
            and (x - 2, y - 2) in game.stone_list[player]
            and (x - 3, y - 3) in game.possible_moves
            and (x + 1, y + 1) in game.possible_moves):
            return True

        if ((x - 1, y - 1) in game.stone_list[player]
            and (x + 1, y + 1) in game.stone_list[player]
            and (x + 2, y + 2) in game.possible_moves
            and (x - 2, y - 2) in game.possible_moves):
            return True

        ######################## Pattern X00X0X
        if ((x - 1, y - 1) in game.stone_list[player]
            and (x - 3, y - 3) in game.stone_list[player]
            and (x - 2, y - 2) in game.possible_moves
            and (x - 4, y - 4) in game.possible_moves
            and (x + 1, y + 1) in game.possible_moves):
            return True

        if ((x + 1, y + 1) in game.stone_list[player]
            and (x - 2, y - 2) in game.stone_list[player]
            and (x + 2, y + 2) in game.possible_moves
            and (x - 3, y - 3) in game.possible_moves
            and (x - 1, y - 1) in game.possible_moves):
            return True
        
        if ((x + 2, y + 2) in game.stone_list[player]
            and (x + 3, y + 3) in game.stone_list[player]
            and (x + 1, y + 1) in game.possible_moves
            and (x + 4, y + 4) in game.possible_moves
            and (x - 1, y - 1) in game.possible_moves):
            return True

        ######################### Pattern X0X00X
        if ((x + 1, y + 1) in game.stone_list[player]
            and (x + 3, y + 3) in game.stone_list[player]
            and (x + 2, y + 2) in game.possible_moves
            and (x + 4, y + 4) in game.possible_moves
            and (x - 1, y - 1) in game.possible_moves):
            return True

        if ((x - 1, y - 1) in game.stone_list[player]
            and (x + 2, y + 2) in game.stone_list[player]
            and (x + 1, y + 1) in game.possible_moves
            and (x - 2, y - 2) in game.possible_moves
            and (x + 3, y + 3) in game.possible_moves):
            return True

        if ((x - 2, y - 2) in game.stone_list[player]
            and (x - 3, y - 3) in game.stone_list[player]
            and (x + 1, y + 1) in game.possible_moves
            and (x - 1, y - 1) in game.possible_moves
            and (x - 4, y - 4) in game.possible_moves):
            return True
        return False

    @staticmethod
    def hasRightDiagonalFreeThree(x, y, game, player):
        ######################### Pattern X000X
        if ((x - 1, y + 1) in game.stone_list[player]
            and (x - 2, y + 2) in game.stone_list[player]
            and (x - 3, y + 3) in game.possible_moves
            and (x + 1, y - 1) in game.possible_moves):
            return True

        if ((x + 1, y - 1) in game.stone_list[player]
            and (x + 2, y - 2) in game.stone_list[player]
            and (x + 3, y - 3) in game.possible_moves
            and (x - 1, y + 1) in game.possible_moves):
            return True

        if ((x + 1, y - 1) in game.stone_list[player]
            and (x - 1, y + 1) in game.stone_list[player]
            and (x - 2, y + 2) in game.possible_moves
            and (x + 2, y - 2) in game.possible_moves):
            return True

        ######################## Pattern X00X0X
        if ((x + 1, y - 1) in game.stone_list[player]
            and (x + 3, y - 3) in game.stone_list[player]
            and (x + 2, y - 2) in game.possible_moves
            and (x + 4, y - 4) in game.possible_moves
            and (x - 1, y + 1) in game.possible_moves):
            return True

        if ((x - 1, y + 1) in game.stone_list[player]
            and (x + 2, y - 2) in game.stone_list[player]
            and (x - 2, y + 2) in game.possible_moves
            and (x + 3, y - 3) in game.possible_moves
            and (x + 1, y - 1) in game.possible_moves):
            return True
        
        if ((x - 2, y + 2) in game.stone_list[player]
            and (x - 3, y + 3) in game.stone_list[player]
            and (x - 1, y + 1) in game.possible_moves
            and (x - 4, y + 4) in game.possible_moves
            and (x + 1, y - 1) in game.possible_moves):
            return True

        ######################### Pattern X0X00X
        if ((x - 1, y + 1) in game.stone_list[player]
            and (x - 3, y + 3) in game.stone_list[player]
            and (x - 2, y + 2) in game.possible_moves
            and (x - 4, y + 4) in game.possible_moves
            and (x + 1, y - 1) in game.possible_moves):
            return True

        if ((x + 1, y - 1) in game.stone_list[player]
            and (x - 2, y + 2) in game.stone_list[player]
            and (x - 1, y + 1) in game.possible_moves
            and (x + 2, y - 2) in game.possible_moves
            and (x - 3, y + 3) in game.possible_moves):
            return True

        if ((x + 2, y - 2) in game.stone_list[player]
            and (x + 3, y - 3) in game.stone_list[player]
            and (x - 1, y + 1) in game.possible_moves
            and (x + 1, y - 1) in game.possible_moves
            and (x + 4, y - 4) in game.possible_moves):
            return True
        return False