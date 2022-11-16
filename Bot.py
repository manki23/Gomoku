from random import choice

class Bot():

    def __init__(self):
        pass

    def getNextMove(self, possible_moves, stone_list, player):
        return choice(possible_moves)