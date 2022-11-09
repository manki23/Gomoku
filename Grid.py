class Board():
    def __init__(self, goban_size=19) -> None:
        self.goban_size = goban_size
        self.black_board = 1 << goban_size ** 2
        self.white_board = 1 << goban_size ** 2
    
    def putStone(self, x, y, board):
        shift = self.goban_size ** 2 - 1 - (self.goban_size * x + y)
        board |= 1 << shift
        return board

    def displayBoard(self, board):
        board = bin(board)[2:]
        print('----------')
        for i in range(1, len(board)):
            if i % self.goban_size == 0:
                print(board[i])
            else:
                print(board[i], end='')
        print('\n----------')