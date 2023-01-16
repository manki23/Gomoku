from CheckRules import CheckRules
from CheckHeuristic import CheckHeuristic
from collections import deque, defaultdict


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
        stones_captured=None,
        player=BLACK,
        opponent=WHITE,
        goban_size=19,
    ):
        self.reset(stone_list, possible_moves, playable_area, forbidden_moves, player_captures, stones_captured, player, opponent, goban_size)

    def reset(self,
            stone_list=None,
            possible_moves=None,
            playable_area=None,
            forbidden_moves=None,
            player_captures=None,
            stones_captured=None,
            player=BLACK,
            opponent=WHITE,
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
        self.stones_captured = stones_captured if stones_captured is not None else {self.WHITE: [], self.BLACK: []}
        self.last_winning_move = {self.WHITE: None, self.BLACK: None}
        self.gameover = False
        self.show_game = False
        self.turn = 0
        self.goban_size = goban_size        
        self.moves_history = deque([])
        self.playable_area_history = defaultdict(set)
        self.last_move = None
        self.bot_mode = False
        self.bot_move = None

    
    def playOneMove(self, xx, yy):
        # print(f"turn {self.turn} => PLAY :", self.stone_list)
        # input()
        # ADD STONE TO PLAYED LIST:
        self.stone_list[self.player].add((xx, yy))
        # print((xx, yy) in self.possible_moves)
        self.possible_moves.remove((xx, yy))
        if (xx, yy) in self.playable_area:
            self.playable_area.remove((xx, yy))
        self.updateStoneAreaCoordinates(xx, yy)
        self._updateForbiddenMoves()
        # MANAGE CAPTURES:
        captures = CheckRules.getCaptures(xx, yy, self, self.player, self.opponent)
        self.stones_captured[self.player].append(captures)
        self._clearCaptures(captures)
        self.player_captures[self.player] += len(captures)

        self.gameover = self.checkGameOver(xx, yy)
        self.opponent, self.player = self.player, self.BLACK if self.player == self.WHITE else self.WHITE
        self.checkForWin()
        self.turn += 1
        self.last_move =  (xx, yy)
        self.moves_history.append((xx, yy))
        # print(f"turn {self.turn} => PLAY :", self.stone_list)
        # input()


    def revertLastMove(self):
        # print(f"turn {self.turn} => REVERT :", self.stone_list)
        # input()
        self.opponent, self.player = self.player, self.BLACK if self.player == self.WHITE else self.WHITE
        xx, yy = self.moves_history.pop()
        self.last_move = self.moves_history[-1] if self.moves_history else None
        if self.last_winning_move[self.player] == (xx, yy):
            self.last_winning_move[self.player] = None
        # Restore captured stones
        if self.stones_captured[self.player] and CheckRules.wasCaptures(xx, yy, self, self.player, self.stones_captured[self.player][-1]):
            captures = self.stones_captured[self.player].pop()
            self.player_captures[self.player] -= len(captures)
            self._restoreCaptures(captures)
        #self.playable_area -= self.playable_area_history[self.turn]
        self.playable_area = set()
        self.playable_area_history[self.turn] = set()
        self.turn -= 1

        self.playable_area.add((xx, yy))
        self.possible_moves.add((xx, yy))
        # print(xx, yy, self.player, self.stone_list)
        self.stone_list[self.player] -= {(xx, yy)}
        # print(xx, yy, self.player, self.stone_list)

        self._updateForbiddenMoves()
        
        # print(f"turn {self.turn} => REVERT :", self.stone_list)
        # input()

    def updateStoneAreaCoordinates(self, x, y):
        width = 1
        for i in range(-width, width+1):
            for j in range(-width, width+1):
                if (x + i, y + j) in self.possible_moves and (x + i, y + j) not in self.playable_area:
                        self.playable_area.add((x + i, y + j))
                        self.playable_area_history[self.turn].add((x + i, y + j))
    
    def _updateForbiddenMoves(self):
        self.forbidden_moves = {self.WHITE: set(), self.BLACK: set()}
        for (x, y) in self.possible_moves:
            if self._isCreatingDoubleThree(x, y, self.player):
                self.forbidden_moves[self.player].add((x, y))
            elif self._isCreatingDoubleThree(x, y, self.opponent):
                self.forbidden_moves[self.opponent].add((x, y))

    def _isCreatingDoubleThree(self, x, y, player):
        return sum([
            CheckRules.hasHorizontalFreeThree(x, y, self, player),
            CheckRules.hasVerticalFreeThree(x, y, self, player),
            CheckRules.hasRightDiagonalFreeThree(x, y, self, player),
            CheckRules.hasLeftDiagonalFreeThree(x, y, self, player)]) >= 2

    def _clearCaptures(self, captures):
        self.possible_moves |= captures
        self.playable_area |= captures
        self.stone_list[self.opponent] -= captures 
        self.forbidden_moves[self.opponent] -= captures
        self.forbidden_moves[self.player] -= captures

    def _restoreCaptures(self, captures):
        self.possible_moves -= captures
        self.playable_area -= captures
        self.stone_list[self.opponent] |= captures 
    

    def checkGameOver(self, xx, yy):
        aligned = self._hasFiveAligned(xx, yy)
        if self.player_captures[self.player] >= 10 or (aligned and not self.letOpponentPlay(aligned, xx, yy)):
            # print(self.player_captures, len(aligned), aligned)
            # if not self.bot_mode
            print(f"turn: {self.turn} player {self.player} WON !") # TODO: CHANGE VICTORY MANAGEMENT
            return True
        return False

    def _hasFiveAligned(self, x, y):
        return (x, y) in self.stone_list[self.player] and (CheckRules.hasColumn(x, y, self)
                    or CheckRules.hasLeftDiagonal(x, y, self)
                    or CheckRules.hasLine(x, y, self)
                    or CheckRules.hasRightDiagonal(x, y, self))

    def letOpponentPlay(self, aligned, x, y):
        for x, y in aligned:
            # Check if we can cature one aligned stone
            if CheckRules.getOpponentCaptures(x, y, self):
                if self.last_winning_move[self.player] is not None:
                    return False
                # print("Can capture one line stone")
                self.last_winning_move[self.player] = (x, y)
                return True
        for x, y in self.stone_list[self.player] - aligned:
            # check if the opponent can win by capture
            if self.player_captures[self.opponent] == 8 and CheckRules.getOpponentCaptures(x, y, self):
                # print("opponent can win by capture")
                return True
        return False

    def checkForWin(self):
        if self.last_winning_move[self.player] is not None and self.checkGameOver(*(self.last_winning_move[self.player])):
            self.gameover = True
        elif self.last_winning_move[self.player]:
            self.last_winning_move[self.player] = None
        return self.gameover
