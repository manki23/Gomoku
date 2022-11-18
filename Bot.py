from random import choice

class Bot():

    @staticmethod
    def getNextMove(possible_moves, stone_list, player, opponent):
        return choice(list(possible_moves))