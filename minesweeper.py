import os
from sys import stdin
from random import sample

WELCOME = 'Welcome to mine sweeper!\nPlease enter the desired number of rows, columns and mines (R C M) to begin!\n\n'
WRONG_INPUT_FORMAT = 'The input has the wrong format, please try again.'
WRONG_SIZE = 'There can be no more than 20 rows and 20 columns, and no less than 10 squares altogether. Please try again.'
WRONG_MINE_COUNT = 'The number of mines can be no smaller than 1, and no greater than 1/3 of the total number of squares.'
BOARD_ACCEPTED = 'Thank you. Now let\'s play.'
MAKE_YOUR_MOVE = 'Time to make your move.\n'
UNKNOWN_COMMAND = 'Unknown command format.  Format should be (action) (row) (column). Action is either f - flag, or p - pick.'
OUT_OF_BOUNDS = 'Row and/or column out of bounds'
ILLEGAL_FLAGGING = 'Can only flag unknown squares!'
BOOM = 'BOOM'

class MineSweeper:
    def __init__(self, rows, cols, mines):
        self.board = []
        self.mine_mask = []
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.alive = True
        self.playing = True
        self.pristine = True
        self.discovered = 0
        self.history = []

        self.make_empty_board()
        self.make_empty_mine_mask()

    def get_square(self, y, x, display_mines):
        if not display_mines or not self.mine_mask[y][x]:
            return self.board[y][x]
        return 'O'

    def print_board(self, display_mines = False):
        print ''
        print '\n'.join(''.join(self.get_square(y, x, display_mines) for x in xrange(self.cols)) for y in xrange(self.rows))
        print ''

    def make_empty_board(self):
        self.board = [['x' for x in xrange(self.cols)] for y in xrange(self.rows)]

    def make_empty_mine_mask(self):
        self.mine_mask = [[False for x in xrange(self.cols)] for y in xrange(self.rows)]

    def place_mines(self, y, x):
        positions = sample([x for x in xrange(self.rows*self.cols)], self.mines)
        while self.cols*y + x in positions:
            positions = sample([x for x in xrange(self.rows*self.cols)], self.mines)

        for position in positions:
            self.mine_mask[position/self.cols][position%self.cols] = True

    def get_neighbours(self, y, x):
        neighbours = []

        for i in xrange(max(0, y-1), min(self.rows, y+2)):
            for j in xrange(max(0, x-1), min(self.cols, x+2)):
                if i != y or j != x:
                    neighbours.append((i, j))

        return neighbours

    def handle_successful(self, y, x):        
        expanding = [(y,x)] + [neighbour for neighbour in self.get_neighbours(y, x) if self.board[neighbour[0]][neighbour[1]] == 'x']
        while expanding:
            vy, vx = expanding.pop()
            if self.board[vy][vx] == '.' or self.mine_mask[vy][vx]:
                continue

            neighbours = self.get_neighbours(vy, vx)
            mine_count = sum(1 if self.mine_mask[neighbour[0]][neighbour[1]] else 0 for neighbour in neighbours)

            if mine_count == 0:
                self.board[vy][vx] = '.'
                for neighbour in neighbours:
                    neighy, neighx = neighbour
                    if self.board[neighy][neighx] == 'x' and not self.mine_mask[neighy][neighx]:
                        expanding.append(neighbour)
                continue
            self.board[vy][vx] = str(mine_count)

    def play_turn(self):
        self.print_board()

        print MAKE_YOUR_MOVE

        command = stdin.readline().split()

        if len(command) != 3 or not command[0] in 'fp' or not command[1].isdigit() or not command[2].isdigit():
            print UNKNOWN_COMMAND
            return

        flagging = command[0] == 'f'
        r = int(command[1])-1
        c = int(command[2])-1

        if r < 0 or r >= rows or c < 0 or c >= cols:
            print OUT_OF_BOUNDS
            return

        if flagging:
            if not self.board[r][c] in 'fx':
                print ILLEGAL_FLAGGING
                return

            self.board[r][c] = 'f' if self.board[r][c] == 'x' else 'x'

        else:
            if self.pristine:
                self.place_mines(r, c)
                self.pristine = False
            elif self.mine_mask[r][c]:
                print BOOM
                self.print_board(True)
                self.alive = False
                return

            self.handle_successful(r, c)

if __name__ == '__main__':
    rows = -1
    cols = -1
    mines = -1

    os.system('cls')
    print WELCOME

    while True:
        rcm = stdin.readline().split()

        if len(rcm) != 3 or any(not i.isdigit() for i in rcm):
            print WRONG_INPUT_FORMAT
            continue

        r, c, m = map(int, rcm)

        if r < 1 or r > 20 or c < 1 or c > 20 or r*c < 10:
            print WRONG_SIZE
            continue

        if not 0 < m <= r*c/3:
            print WRONG_MINE_COUNT
            continue

        rows = r
        cols = c
        mines = m

        print BOARD_ACCEPTED
        break

    mine_sweeper = MineSweeper(rows, cols, mines)

    while mine_sweeper.alive and mine_sweeper.playing:
        mine_sweeper.play_turn()
