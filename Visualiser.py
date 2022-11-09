import pygame
import sys


DEBUG = 1

class Color():
    black = (0, 0, 0)
    white = (200, 200, 200)
    brown = (214, 137, 16)

class Visualiser():
    def __init__(self, goban_size=19) -> None:
        pygame.init()
        self.goban_size = goban_size - 1
        self.window_width = 1000
        self.window_height = 800
        self.block_size = min(600 // self.goban_size, 150)
        self.grid_size = self.block_size * self.goban_size
        self.stone_radius = self.block_size // 3
        self.x_padding = (self.window_width - self.grid_size) // 2
        self.y_padding = (self.window_height - self.grid_size) // 2

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.clock = pygame.time.Clock()
        self.screen.fill(Color.black)
        self.display()

    def display(self) -> None:
        while True:
            self.drawGrid()
            self.shadowDisplay()
            self.clock.tick(60)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

    def drawGrid(self) -> None:
        self.screen.fill(Color.black)
        for x in range(self.goban_size):
            for y in range(self.goban_size):
                rect = pygame.Rect(self.x_padding + x * self.block_size,
                                   self.y_padding + y * self.block_size,
                                   self.block_size,
                                   self.block_size)
                pygame.draw.rect(self.screen, Color.white, rect, 1)
    
    def shadowDisplay(self) -> None:
        x_mouse, y_mouse = pygame.mouse.get_pos()
        x = self._getCursorZone(x_mouse, self.x_padding)
        y = self._getCursorZone(y_mouse, self.y_padding)
        if DEBUG:
            print(x, y)
            print('Mouse position :', pygame.mouse.get_pos())
        zone_padding = self.block_size // 2
        if self._moreOrLess(x_mouse, zone_padding, self.x_padding, x) and self._moreOrLess(y_mouse, zone_padding, self.y_padding, y):
            pygame.draw.circle(self.screen, Color.white, (x, y), self.stone_radius)
        

    def _getCursorZone(self, mouse_pos, padding) -> int:
        return int(((mouse_pos - padding) / self.block_size) + 0.5) * self.block_size + padding
    
    def _moreOrLess(self, cursor, stone_padding, window_padding, ref) -> bool:
        return ((cursor <= ref + stone_padding)
                and (cursor >= ref - stone_padding)
                and (window_padding - stone_padding <= cursor <= self.grid_size + window_padding + stone_padding))


if __name__ == '__main__':
    viz = Visualiser()