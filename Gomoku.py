import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
from Game import Game
from threading import Thread
from Bot2 import Bot
import cProfile

DEBUG = 0

class Color():
    black = (0, 0, 0)
    grey = (200, 200, 200)
    white = (255, 255, 255)
    back_brown = (196, 134, 95)
    goban_brown = (249, 235, 210)
    line_brown = (198, 135, 104)
    red = (192, 57, 43)

class Gomoku():
    def __init__(self, goban_size=19) -> None:
        pygame.init()
        self.goban_size = goban_size
        self.square_number = goban_size - 1
        self.window_width = 1000
        self.window_height = 800
        self.block_size = min(600 // self.square_number, 150)
        self.grid_size = self.block_size * self.square_number
        self.stone_radius = self.block_size // 3
        self.x_padding = (self.window_width - self.grid_size) // 2
        self.y_padding = (self.window_height - self.grid_size) // 2
        self.WHITE = 2
        self.BLACK = 1
        self.EMPTY = 0

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('Gomoku')
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.clock = pygame.time.Clock()
        self.clock.tick(60)

        self.mode = {self.WHITE: "HUMAN", self.BLACK: "HUMAN"}

        self.game = Game()

        self.bot_thread = None


    def resetGame(self):
        self.game.reset()

    def displayStart(self):
        # START
        self.start_text = self.font.render("START", True, Color.white)
        self.start_text_rect = self.start_text.get_rect()
        self.start_text_rect.center = (self.window_width // 2, self.window_height // 2)
        self.screen.blit(self.start_text, self.start_text_rect)


    def displayPlayersTitle(self):
        # LEFT TITLE
        self.player1_text = self.font.render("PLAYER 1", True, Color.white)
        self.player1_text_rect = self.player1_text.get_rect()
        self.player1_text_rect.center = (1 * self.window_width // 5, 1 * self.window_height // 4)
        self.screen.blit(self.player1_text, self.player1_text_rect)

        # DISPLAY BLACK STONE
        pygame.draw.circle(self.screen, Color.black, (1 * self.window_width // 5, 2 * self.window_height // 5), self.stone_radius * 3)

        # RIGHT TITLE
        self.player2_text = self.font.render("PLAYER 2", True, Color.white)
        self.player2_text_rect = self.player2_text.get_rect()
        self.player2_text_rect.center = (4 * self.window_width // 5, 1 * self.window_height // 4)
        self.screen.blit(self.player2_text, self.player2_text_rect)

        # DISPLAY WHITE STONE
        pygame.draw.circle(self.screen, Color.white,(4 * self.window_width // 5, 2 * self.window_height // 5), self.stone_radius * 3)


    def displayP1Settings(self):
        # PLAYER 1 MODE
        self.p1_mode_text = self.font.render(self.mode[self.BLACK], True, Color.white)
        self.p1_mode_text_rect = self.p1_mode_text.get_rect()
        self.p1_mode_text_rect.center = (1 * self.window_width // 5, 3 * self.window_height // 5)
        background = pygame.Rect(1 * self.window_width // 5 - 80, # x
                                 3 * self.window_height // 5 - 35, # y
                                 160, # width
                                 65) # height
        pygame.draw.rect(self.screen, Color.white, background, 1)
        self.screen.blit(self.p1_mode_text, self.p1_mode_text_rect)


    def displayP2Settings(self):
        # PLAYER 2 MODE
        self.p2_mode_text = self.font.render(self.mode[self.WHITE], True, Color.white)
        self.p2_mode_text_rect = self.p2_mode_text.get_rect()
        self.p2_mode_text_rect.center = (4 * self.window_width // 5, 3 * self.window_height // 5)
        background = pygame.Rect(4 * self.window_width // 5 - 80, # x
                                 3 * self.window_height // 5 - 35, # y
                                 160, # width
                                 65) # height
        pygame.draw.rect(self.screen, Color.white, background, 1)
        self.screen.blit(self.p2_mode_text, self.p2_mode_text_rect)


    def updateModeText(self, text):
        return "AI" if text == "HUMAN" else "HUMAN"


    def menu(self):
        self.game.show_game = False
        while not self.game.show_game:
            self.screen.fill(Color.back_brown)
            self.checkEvents()
            self.displayStart()
            self.displayPlayersTitle()
            self.displayP1Settings()
            self.displayP2Settings()
            pygame.display.update()
        self.launch_game()

    def playNextMove(self, game):
        if len(game.possible_moves) > 0:

            print(self.bot_thread)
            self.bot_thread = Thread(target=Bot.getNextMove, args=(game, ))
            self.bot_thread.start()
            print(self.bot_thread)
            # (x, y) = Bot.getNextMove(self)
            # game.playOneMove(*game.bot_move)
            # game.bot_move = None
            # print("DEBUG:", CheckHeuristic.getPatternDict(self.game.stone_list, self.game.opponent, self.game.player, self.game.possible_moves, self.game.forbidden_moves, True))
            # print("DEBUG:", CheckHeuristic.getPatternDict(self.game, self.game.possible_moves, self.game.forbidden_moves, True))

    def launch_game(self) -> None:
        self.game.gameover = False
        while self.game.show_game:
            self.drawGrid()
            self.drawBoard()
            self.drawCapture()
            self.drawExitButton()
            self.shadowDisplay()
            self.checkEvents()
            if self.mode[self.game.player] == "AI" and not self.game.gameover and self.game.bot_move is None and self.bot_thread is None:
                self.playNextMove(self.game)
            elif self.mode[self.game.player] == "AI" and not self.game.gameover and self.game.bot_move is not None:
                print(self.game.bot_move)
                self.game.playOneMove(*self.game.bot_move)
                self.game.bot_move = None
                self.bot_thread = None
            pygame.display.update()
        self.menu()
 

    def drawGrid(self) -> None:
        self.screen.fill(Color.back_brown)
        board = pygame.Rect(self.x_padding - self.block_size // 2,
                            self.y_padding - self.block_size // 2,
                            self.grid_size + self.block_size,
                            self.grid_size + self.block_size)
        pygame.draw.rect(self.screen, Color.goban_brown, board, 0, border_radius=10)
        grid_border = pygame.Rect(self.x_padding, self.y_padding, self.grid_size, self.grid_size)
        pygame.draw.rect(self.screen, Color.line_brown, grid_border, 2)
        
        for x in range(self.square_number):
            for y in range(self.square_number):
                rect = pygame.Rect(self.x_padding + x * self.block_size,
                                   self.y_padding + y * self.block_size,
                                   self.block_size,
                                   self.block_size)
                pygame.draw.rect(self.screen, Color.line_brown, rect, 1)

    def drawBoard(self) -> None:
        for (x, y) in self.game.stone_list[self.BLACK]:
            pos = (x * self.block_size + self.x_padding, y * self.block_size + self.y_padding)
            pygame.draw.circle(self.screen, Color.black, pos, self.stone_radius)
        for (x, y) in self.game.stone_list[self.WHITE]:
            pos = (x * self.block_size + self.x_padding, y * self.block_size + self.y_padding)
            pygame.draw.circle(self.screen, Color.white, pos, self.stone_radius)
        if self.game.moves_history:
            x, y = self.game.moves_history[-1]
            pos = (x * self.block_size + self.x_padding, y * self.block_size + self.y_padding)
            pygame.draw.circle(self.screen, Color.red, pos, self.stone_radius // 3)
        
    
    def drawCapture(self) -> None:
        left_captures = str(self.game.player_captures[self.WHITE] // 2)
        right_captures = str(self.game.player_captures[self.BLACK] // 2)
        color = Color.black if self.game.player == self.BLACK else Color.white
        pygame.draw.circle(self.screen, color, (self.window_width // 2, (self.y_padding - self.block_size // 2) // 2), self.stone_radius * 2)

        self.turn_text = self.font.render(f"TURN: {self.game.turn}", True, Color.goban_brown)
        self.turn_text_rect = self.turn_text.get_rect()
        self.turn_text_rect.center = (self.window_width // 2, 14 * self.window_height // 15)
        self.screen.blit(self.turn_text, self.turn_text_rect)


        self.right_text = self.font.render(right_captures, True, Color.goban_brown)
        self.right_text_rect = self.right_text.get_rect()
        self.right_text_rect.center = (self.x_padding // 3, self.y_padding)

        self.left_text = self.font.render(left_captures, True, Color.goban_brown)
        self.left_text_rect = self.left_text.get_rect()
        self.left_text_rect.center = (self.window_width - self.x_padding // 3, self.y_padding)

        self.screen.blit(self.right_text, self.right_text_rect)
        self.screen.blit(self.left_text, self.left_text_rect)
        pygame.draw.circle(self.screen, Color.black, (self.x_padding // 3, self.y_padding - self.block_size), self.stone_radius)
        pygame.draw.circle(self.screen, Color.white,(self.window_width - self.x_padding // 3, self.y_padding - self.block_size), self.stone_radius)


    def drawExitButton(self) -> None:
        self.exit_button_text = self.font.render("EXIT", True, Color.goban_brown)
        self.exit_button_text_rect = self.exit_button_text.get_rect()
        self.exit_button_text_rect.center = (1 * self.window_width // 12, 11 * self.window_height // 12)
        self.screen.blit(self.exit_button_text, self.exit_button_text_rect)


    def shadowDisplay(self) -> None:
        if self.game.gameover:
            return
        x_mouse, y_mouse = pygame.mouse.get_pos()
        x = self._getCursorZone(x_mouse, self.x_padding)
        y = self._getCursorZone(y_mouse, self.y_padding)

        zone_padding = self.block_size // 2
        xx = (x - self.x_padding) // self.block_size
        yy = (y - self.y_padding) // self.block_size
        if (xx, yy) in (self.game.possible_moves - self.game.forbidden_moves[self.game.player]):
            pygame.draw.circle(self.screen, Color.grey, (x, y), self.stone_radius)



    def checkMousePressed(self) -> None:
        x_mouse, y_mouse = pygame.mouse.get_pos()
        zone_padding = self.block_size // 2
        x = self._getCursorZone(x_mouse, self.x_padding)
        y = self._getCursorZone(y_mouse, self.y_padding)

        if (self._moreOrLess(x_mouse, zone_padding, self.x_padding, x)
            and self._moreOrLess(y_mouse, zone_padding, self.y_padding, y)):
            xx = (x - self.x_padding) // self.block_size
            yy = (y - self.y_padding) // self.block_size

            if (xx, yy) in (self.game.possible_moves - self.game.forbidden_moves[self.game.player]):
                self.game.playOneMove(xx, yy)


    def checkEvents(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                # print(event.pos)
                if self.game.show_game and self.exit_button_text_rect.collidepoint(event.pos):
                    self.resetGame()
                elif self.game.show_game and self.mode[self.game.player] == "HUMAN" and not self.game.gameover:
                    self.checkMousePressed()
                elif self.start_text_rect.collidepoint(event.pos):
                    self.game.show_game = True
                elif self.p1_mode_text_rect.collidepoint(event.pos):
                    self.mode[self.BLACK] = self.updateModeText(self.mode[self.BLACK])
                elif self.p2_mode_text_rect.collidepoint(event.pos):
                    self.mode[self.WHITE] = self.updateModeText(self.mode[self.WHITE])
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_a:
                    self.game.opponent = self.game.player
                    self.game.player = self.BLACK if self.game.player == self.WHITE else self.WHITE
                elif event.key == pygame.K_r:
                    self.resetGame()

    def _getCursorZone(self, mouse_pos, padding) -> int:
        return int(((mouse_pos - padding) / self.block_size) + 0.5) * self.block_size + padding
    
    def _moreOrLess(self, cursor, stone_padding, window_padding, ref) -> bool:
        return ((cursor <= ref + stone_padding)
                and (cursor >= ref - stone_padding)
                and (window_padding - stone_padding <= cursor <= self.grid_size + window_padding + stone_padding))


if __name__ == '__main__':
    
    viz = Gomoku(19)
    viz.launch_game()