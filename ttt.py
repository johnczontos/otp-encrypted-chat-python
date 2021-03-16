# Tik Tac Toe w/ Board clasee

import os


class Board():
    PIECE_X = '×'
    PIECE_O = '○'
    PIECE_EMPTY = '-'
    BLANKBOARD = [[PIECE_EMPTY]*3,
                  [PIECE_EMPTY]*3,
                  [PIECE_EMPTY]*3]

    def __init__(self):
        self.board = self.BLANKBOARD
        self.turn = self.PIECE_O
        # self.display()

    def __getitem__(self, index):
        return self.board[index // 3][index % 3]

    def __setitem__(self, index, value):
        self.board[index // 3][index % 3] = value

    def display(self):
        os.system("clear")
        print("""type a number to make your move.\n0 1 2\n3 4 5\n6 7 8\n""")
        print('\n'.join(' '.join(row) for row in self.board))

    def check_idx(self, index):
        if (not (index in range(0, 9))) or self[index] != self.PIECE_EMPTY:
            return False
        return True

    def make_move(self):
        self.display()

        while True:
            idx = input("type index of move: ")
            if idx.isnumeric() and self.check_idx(int(idx)):
                break
            self.display()
            print("invalid move")

        self.turn = self.PIECE_O if self.turn == self.PIECE_X \
            else self.PIECE_X

        self[int(idx)] = self.turn

        if self.check_for_win():
            print("you won!")
            play = input("play again?(y/n)")
            if play.startswith('y'):
                # clear board
                for i in range(0, 9):
                    self[i] = self.PIECE_EMPTY
            else:
                exit()
        return idx

    def recv_move(self, idx):
        self.turn = self.PIECE_O if self.turn == self.PIECE_X \
            else self.PIECE_X
        self[int(idx)] = self.turn
        self.display()
        if self.check_for_win():
            print("you lost!")
            quit = input("play again?(y/n)")
            if quit.startswith('y'):
                # clear board
                for i in range(0, 9):
                    self[i] = self.PIECE_EMPTY
            else:
                exit()

    def check_line(self, iterable, player):
        return all(map(lambda piece: piece == player, iterable))

    def check_for_win(self):
        for player in [self.PIECE_X, self.PIECE_O]:
            # 1. Check all rows
            for row in self.board:
                if self.check_line(row, player):
                    return player

            # 2. Check all columns
            for column in zip(*self.board):
                if self.check_line(column, player):
                    return player

            # 3. Check the two diagonals
            diagonals = [
                [self[0], self[4], self[8]],
                [self[2], self[4], self[6]],
            ]
            for diagonal in diagonals:
                if self.check_line(diagonal, player):
                    return player
        return None


def main():
    board = Board()
    while True:
        board.make_move()


if __name__ == "__main__":
    main()
