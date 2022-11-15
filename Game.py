import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
import sys
from CheckRules import CheckRules

DEBUG = 0

class Color():
    black = (0, 0, 0)
    grey = (200, 200, 200)
    white = (255, 255, 255)
    back_brown = (196, 134, 95)
    goban_brown = (249, 235, 210)
    line_brown = (198, 135, 104)

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

        self.board = [0] * goban_size ** 2
        self.stone_list = {self.WHITE: set(), self.BLACK: set()}
        self.possible_moves = set((x, y) for x in range(0, goban_size) for y in range(0, goban_size))
        self.forbiden_move = {self.WHITE: set(), self.BLACK: set()}
        self.player_captures = {self.WHITE: 0, self.BLACK: 0}
        # self.stones_graph = {}
        self.player = 1

        self.display()

    def display(self) -> None:
        self.clock.tick(60)
        while True:
            left_captures = str(self.player_captures[self.WHITE])
            right_captures = str(self.player_captures[self.BLACK])
            self.drawGrid()
            self.drawBoard()
            self.drawCapture(right_captures, left_captures)
            self.shadowDisplay()
            pygame.display.update()
            self.checkEvents()
 
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
    
    def drawCapture(self, right_captures, left_captures) -> None:
        color = Color.black if self.player == self.BLACK else Color.white
        pygame.draw.circle(self.screen, color, (self.window_width // 2, self.y_padding - self.block_size * 2), self.stone_radius * 2)

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

    def _getPossibleMoves(self):
        self.possible_moves = self.possible_moves - (self.stone_list[self.WHITE] | self.stone_list[self.BLACK])
        self.forbiden_move = {self.WHITE: set(), self.BLACK: set()}
        for (x, y) in self.possible_moves:
            if self._isCreatingDoubleThree(x, y):
                self.forbiden_move[self.player].add((x, y))
        return self.possible_moves - self.forbiden_move[self.player]

    def shadowDisplay(self) -> None:
        x_mouse, y_mouse = pygame.mouse.get_pos()
        x = self._getCursorZone(x_mouse, self.x_padding)
        y = self._getCursorZone(y_mouse, self.y_padding)
        if DEBUG:
            print(x, y)
            print('Mouse position :', pygame.mouse.get_pos())
        zone_padding = self.block_size // 2
        xx = (x - self.x_padding) // self.block_size
        yy = (y - self.y_padding) // self.block_size
        if (xx, yy) in self._getPossibleMoves():
            pygame.draw.circle(self.screen, Color.grey, (x, y), self.stone_radius)


    def _isCreatingDoubleThree(self, x, y):
        return sum([
            CheckRules._hasColumnThree(x, y, self.stone_list, self.player, self.goban_size),
            CheckRules._hasLeftDiagonalThree(x, y, self.stone_list, self.player, self.goban_size),
            CheckRules._hasRightDiagonalThree(x, y, self.stone_list, self.player, self.goban_size),
            CheckRules._hasLineThree(x, y, self.stone_list, self.player, self.goban_size)]) >= 2

    def _hasWon(self, x, y):
        return (CheckRules._hasColumn(x, y, self.stone_list, self.player, self.goban_size)
                    or CheckRules._hasLeftDiagonal(x, y, self.stone_list, self.player, self.goban_size)
                    or CheckRules._hasLine(x, y, self.stone_list, self.player, self.goban_size)
                    or CheckRules._hasRightDiagonal(x, y, self.stone_list, self.player, self.goban_size))

    def _clearCaptures(self, captures, opponent):
        self.possible_moves |= captures
        self.stone_list[opponent] -= captures 
        self.forbiden_move[opponent] -= captures
        self.forbiden_move[self.player] -= captures

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
                # ADD STONE TO PLAYED LIST:
                self.stone_list[self.player].add((xx, yy))
                # MANAGE CAPTURE:
                opponent = self.BLACK if self.player == self.WHITE else self.WHITE
                captures = CheckRules._getCaptures(xx, yy, self.stone_list, self.player, opponent)
                self._clearCaptures(captures, opponent)
                self.player_captures[self.player] += len(captures)
                if self.player_captures[self.player] >= 10 or self._hasWon(xx, yy):
                    print(f"player {self.player} WON !")

                # self.player = self.BLACK if self.player == self.WHITE else self.WHITE

    def checkEvents(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                self.checkMousePressed()
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_a:
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