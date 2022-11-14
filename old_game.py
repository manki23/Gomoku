from Visualiser import Visualiser


class Player():
    def __init__(self, color: str, mode: str):
        self.color = color
        self.mode = mode
        self.capture = 0

class Game():
    def __init__(self):
        self.player_black = Player(color="black", mode="human")
        self.player_white = Player(color="white", mode="human")
        self.goban = Grid()
        self.visualiser = Visualiser(19)
        self.current_player = self.player_black
        self.game_over = False

    def start(self):
        while not self.game_over:
            
            


        