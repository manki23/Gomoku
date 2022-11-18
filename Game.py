import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
import sys
from CheckRules import CheckRules
from Bot import Bot

DEBUG = 0

class Color():
    black = (0, 0, 0)
    grey = (200, 200, 200)
    white = (255, 255, 255)
    back_brown = (196, 134, 95)
    goban_brown = (249, 235, 210)
    line_brown = (198, 135, 104)
    red = (192, 57, 43)

class Player():
    def __init__(self, color: str, mode: str):
        self.color = color
        self.mode = mode
        self.capture = 0

class Visualiser():
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
        self.resetGame()
        self.mode = {self.WHITE: "HUMAN", self.BLACK: "HUMAN"}


    def resetGame(self):
        self.player = self.BLACK
        self.opponent = self.WHITE
        self.stone_list = {self.WHITE: set(), self.BLACK: set()}
        self.possible_moves = set((x, y) for x in range(0, self.goban_size) for y in range(0, self.goban_size))
        self.forbidden_move = {self.WHITE: set(), self.BLACK: set()}
        self.player_captures = {self.WHITE: 0, self.BLACK: 0}
        self.gameover = False
        self.show_game = False

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
        self.show_game = False
        while not self.show_game:
            self.screen.fill(Color.back_brown)
            self.checkEvents()
            self.displayStart()
            self.displayPlayersTitle()
            self.displayP1Settings()
            self.displayP2Settings()
            pygame.display.update()
        self.launch_game()


    def playNextMove(self):
        if len(self.possible_moves) > 0:
            (x, y) = Bot.getNextMove(self.possible_moves, self.stone_list, self.player, self.opponent)
            self.playOneMove(x, y)


    def launch_game(self) -> None:
        self.gameover = False
        while self.show_game:
            self.drawGrid()
            self.drawBoard()
            self.drawCapture()
            self.drawExitButton()
            self.shadowDisplay()
            self.checkEvents()
            if self.mode[self.player] == "AI":
                self.playNextMove()
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
        for (x, y) in self.stone_list[self.BLACK]:
            pos = (x * self.block_size + self.x_padding, y * self.block_size + self.y_padding)
            pygame.draw.circle(self.screen, Color.black, pos, self.stone_radius)
        for (x, y) in self.stone_list[self.WHITE]:
            pos = (x * self.block_size + self.x_padding, y * self.block_size + self.y_padding)
            pygame.draw.circle(self.screen, Color.white, pos, self.stone_radius)
    
    def drawCapture(self) -> None:
        left_captures = str(self.player_captures[self.WHITE])
        right_captures = str(self.player_captures[self.BLACK])
        color = Color.black if self.player == self.BLACK else Color.white
        pygame.draw.circle(self.screen, color, (self.window_width // 2, (self.y_padding - self.block_size // 2) // 2), self.stone_radius * 2)

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
        self.exit_button_text = self.font.render("EXIT", True, Color.white)
        self.exit_button_text_rect = self.exit_button_text.get_rect()
        self.exit_button_text_rect.center = (1 * self.window_width // 12, 11 * self.window_height // 12)
        self.screen.blit(self.exit_button_text, self.exit_button_text_rect)

    def _getPossibleMoves(self):
        self.possible_moves = self.possible_moves - (self.stone_list[self.WHITE] | self.stone_list[self.BLACK])
        return self.possible_moves - self.forbidden_move[self.player]

    def _updateForbiddenMoves(self):
        self.forbidden_move = {self.WHITE: set(), self.BLACK: set()}
        for (x, y) in self.possible_moves:
            if self._isCreatingDoubleThree(x, y, self.player):
                self.forbidden_move[self.player].add((x, y))
            elif self._isCreatingDoubleThree(x, y, self.opponent):
                self.forbidden_move[self.opponent].add((x, y))

    def shadowDisplay(self) -> None:
        if self.gameover:
            return
        x_mouse, y_mouse = pygame.mouse.get_pos()
        x = self._getCursorZone(x_mouse, self.x_padding)
        y = self._getCursorZone(y_mouse, self.y_padding)

        zone_padding = self.block_size // 2
        xx = (x - self.x_padding) // self.block_size
        yy = (y - self.y_padding) // self.block_size
        if (xx, yy) in (self.possible_moves - self.forbidden_move[self.player]):
            pygame.draw.circle(self.screen, Color.grey, (x, y), self.stone_radius)


    def _isCreatingDoubleThree(self, x, y, player):
        return sum([
            CheckRules._hasHorizontalFreeThree(x, y, self.stone_list, player, self.possible_moves),
            CheckRules._hasVerticalFreeThree(x, y, self.stone_list, player, self.possible_moves),
            CheckRules._hasRightDiagonalFreeThree(x, y, self.stone_list, player, self.possible_moves),
            CheckRules._hasLeftDiagonalFreeThree(x, y, self.stone_list, player, self.possible_moves)]) >= 2

    def _clearCaptures(self, captures):
        self.possible_moves |= captures
        self.stone_list[self.opponent] -= captures 
        self.forbidden_move[self.opponent] -= captures
        self.forbidden_move[self.player] -= captures

    def playOneMove(self, xx, yy):
        # ADD STONE TO PLAYED LIST:
        self.stone_list[self.player].add((xx, yy))
        self.possible_moves.remove((xx, yy))
        self._updateForbiddenMoves()
        # MANAGE CAPTURE:
        captures = CheckRules._getCaptures(xx, yy, self.stone_list, self.player, self.opponent)
        self._clearCaptures(captures)
        self.player_captures[self.player] += len(captures)
        self.checkGameOver(xx, yy)
        self.opponent, self.player = self.player, self.BLACK if self.player == self.WHITE else self.WHITE

    def _hasFiveAligned(self, x, y):
        return (CheckRules._hasColumn(x, y, self.stone_list, self.player, self.goban_size)
                    or CheckRules._hasLeftDiagonal(x, y, self.stone_list, self.player, self.goban_size)
                    or CheckRules._hasLine(x, y, self.stone_list, self.player, self.goban_size)
                    or CheckRules._hasRightDiagonal(x, y, self.stone_list, self.player, self.goban_size))

    def checkGameOver(self, xx, yy):
        if self.player_captures[self.player] >= 10 or self._hasFiveAligned(xx, yy):
            print(f"player {self.player} WON !") # TODO: CHANGE VICTORY MANAGEMENT
            self.gameover = True

    def checkMousePressed(self) -> None:
        x_mouse, y_mouse = pygame.mouse.get_pos()
        zone_padding = self.block_size // 2
        x = self._getCursorZone(x_mouse, self.x_padding)
        y = self._getCursorZone(y_mouse, self.y_padding)

        if (self._moreOrLess(x_mouse, zone_padding, self.x_padding, x)
            and self._moreOrLess(y_mouse, zone_padding, self.y_padding, y)):
            xx = (x - self.x_padding) // self.block_size
            yy = (y - self.y_padding) // self.block_size

            if (xx, yy) in self._getPossibleMoves():
                self.playOneMove(xx, yy)


    def checkEvents(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                # print(event.pos)
                if self.show_game and self.exit_button_text_rect.collidepoint(event.pos):
                    self.resetGame()
                elif self.show_game and self.mode[self.player] == "HUMAN" and not self.gameover:
                    self.checkMousePressed()
                elif self.start_text_rect.collidepoint(event.pos):
                    self.show_game = True
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
                    self.opponent = self.player
                    self.player = self.BLACK if self.player == self.WHITE else self.WHITE
                elif event.key == pygame.K_r:
                    self.stone_list = {self.WHITE : set(), self.BLACK : set()}
                    self.possible_moves = set((x, y) for x in range(0, self.goban_size) for y in range(0, self.goban_size))

    def _getCursorZone(self, mouse_pos, padding) -> int:
        return int(((mouse_pos - padding) / self.block_size) + 0.5) * self.block_size + padding
    
    def _moreOrLess(self, cursor, stone_padding, window_padding, ref) -> bool:
        return ((cursor <= ref + stone_padding)
                and (cursor >= ref - stone_padding)
                and (window_padding - stone_padding <= cursor <= self.grid_size + window_padding + stone_padding))


if __name__ == '__main__':
    
    viz = Visualiser(19)
    viz.launch_game()