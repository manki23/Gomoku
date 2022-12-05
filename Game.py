import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
import sys
from CheckRules import CheckRules
from Bot import Bot
from CheckHeuristic import CheckHeuristic
import cProfile
from collections import deque

DEBUG = 0

class Color():
    black = (0, 0, 0)
    grey = (200, 200, 200)
    white = (255, 255, 255)
    back_brown = (196, 134, 95)
    goban_brown = (249, 235, 210)
    line_brown = (198, 135, 104)
    red = (192, 57, 43)

class Game():
    WHITE = 2
    BLACK = 1
    EMPTY = 0
    def __init__(self,
        stone_list=None,
        possible_moves=None,
        playable_area=None,
        forbidden_moves=None,
        player_captures=None,
        player=Game.BLACK,
        opponent=Game.WHITE,
        goban_size=19,
    ):
        self.reset(stone_list, possible_moves, playable_area, forbidden_moves, player_captures, player, opponent, goban_size)

    def reset(self,
            stone_list=None,
            possible_moves=None,
            playable_area=None,
            forbidden_moves=None,
            player_captures=None,
            player=Game.BLACK,
            opponent=Game.WHITE,
            goban_size=19,
        ):
        self.player = player
        self.opponent = opponent
        self.stone_list = stone_list if stone_list is not None else {self.WHITE: set(), self.BLACK: set()}
        self.possible_moves = possible_moves if possible_moves is not None else set((x, y) for x in range(0, goban_size) for y in range(0, goban_size))
        low = (goban_size // 2) - 1
        high = (goban_size // 2) + 2
        self.playable_area = playable_area if playable_area is not None else set((x, y) for x in range(low, high) for y in range(low, high))
        self.forbidden_moves = forbidden_moves if forbidden_moves is not None else {self.WHITE: set(), self.BLACK: set()}
        self.player_captures = player_captures if player_captures is not None else {self.WHITE: 0, self.BLACK: 0}
        self.last_winning_move = {self.WHITE: None, self.BLACK: None}
        self.gameover = False
        self.show_game = False
        self.turns = 0
        self.goban_size = goban_size        
        self.moves_history = deque([])
    
    def playOneMove(self, xx, yy):
        # ADD STONE TO PLAYED LIST:
        self.stone_list[self.player].add((xx, yy))
        self.possible_moves.remove((xx, yy))
        if (xx, yy) in self.playable_area:
            self.playable_area.remove((xx, yy))
        self.updateStoneAreaCoordinates(xx, yy)
        self._updateForbiddenMoves()
        # MANAGE CAPTURE:
        captures = CheckRules._getCaptures(xx, yy, self, player)
        self._clearCaptures(captures)
        self.player_captures[self.player] += len(captures)

        self.gameover = self.checkGameOver(xx, yy)
        self.opponent, self.player = self.player, self.BLACK if self.player == self.WHITE else self.WHITE
        self.checkForWin()
        self.turns += 1
        self.last_move =  (xx, yy)
        self.moves_history.append((xx, yy))

    def revertLastMove(self):
        pass

    def updateStoneAreaCoordinates(self, x, y):
        for i in range(-2, 3):
            for j in range(-2, 3):
                if (x + i, y + j) in self.possible_moves:
                    self.playable_area.add((x + i, y + j))
    
    def _updateForbiddenMoves(self):
        self.forbidden_moves = {self.WHITE: set(), self.BLACK: set()}
        for (x, y) in self.possible_moves:
            if self._isCreatingDoubleThree(x, y, self.player):
                self.forbidden_moves[self.player].add((x, y))
            elif self._isCreatingDoubleThree(x, y, self.opponent):
                self.forbidden_moves[self.opponent].add((x, y))

    def _isCreatingDoubleThree(self, x, y, player):
        return sum([
            CheckRules._hasHorizontalFreeThree(x, y, self, player),
            CheckRules._hasVerticalFreeThree(x, y, self, player),
            CheckRules._hasRightDiagonalFreeThree(x, y, self, player),
            CheckRules._hasLeftDiagonalFreeThree(x, y, self, player)]) >= 2

    def _clearCaptures(self, captures):
        self.possible_moves |= captures
        self.playable_area |= captures
        self.stone_list[self.opponent] -= captures 
        self.forbidden_moves[self.opponent] -= captures
        self.forbidden_moves[self.player] -= captures
    

    def checkGameOver(self, xx, yy):
        aligned = self._hasFiveAligned(xx, yy)
        if self.player_captures[self.player] >= 10 or (aligned and not self.letOpponentPlay(aligned, xx, yy)):
            print(f"player {self.player} WON !") # TODO: CHANGE VICTORY MANAGEMENT
            return True
        return False

    def _hasFiveAligned(self, x, y):
        return (x, y) in self.stone_list[self.player] and (CheckRules._hasColumn(x, y, self)
                    or CheckRules._hasLeftDiagonal(x, y, self)
                    or CheckRules._hasLine(x, y, self)
                    or CheckRules._hasRightDiagonal(x, y, self))

    def letOpponentPlay(self, aligned, x, y):
        for x, y in aligned:
            # Check if we can cature one aligned stone
            if CheckRules._getOpponentCaptures(x, y, self):
                if self.last_winning_move[self.player] is not None:
                    return False
                # print("Can capture one line stone")
                self.last_winning_move[self.player] = (x, y)
                return True
        for x, y in self.stone_list[self.player] - aligned:
            # check if the opponent can win by capture
            if self.player_captures[self.opponent] == 8 and CheckRules._getOpponentCaptures(x, y, self):
                # print("opponent can win by capture")
                return True
        return False

    def checkForWin(self):
        if self.last_winning_move[self.player] is not None and self.checkGameOver(*(self.last_winning_move[self.player])):
            self.gameover = True
        elif self.last_winning_move[self.player]:
            self.last_winning_move[self.player] = None
        return self.gameover


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

        self.mode = {self.WHITE: "HUMAN", self.BLACK: "HUMAN"}

        self.game = Game()


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


    def playNextMove(self):
        if len(self.game.possible_moves) > 0:
            (x, y) = Bot.getNextMove(self.game)
            self.playOneMove(x, y)
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
            if self.mode[self.game.player] == "AI" and not self.game.gameover:
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

        self.turns_text = self.font.render(f"TURN: {self.game.turns}", True, Color.goban_brown)
        self.turns_text_rect = self.turns_text.get_rect()
        self.turns_text_rect.center = (self.window_width // 2, 14 * self.window_height // 15)
        self.screen.blit(self.turns_text, self.turns_text_rect)


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
                self.playOneMove(xx, yy)


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
    
    viz = Visualiser(19)
    viz.launch_game()