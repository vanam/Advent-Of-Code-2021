# https://adventofcode.com/2021/day/4

FILE = 'input.txt'
# FILE = 'input-small.txt'

BINGO_SIZE = 5

# 1. part - play bingo and find who wins


class Bingo:
    MARKED = -1

    def __init__(self, size, board):
        self.size = size
        self.board = board
        self.won = False

    def __str__(self):
        return str(self.board)

    def mark(self, number) -> bool:
        # Do not mark other numbers after win
        if self.won:
            return False

        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.board[i][j] == number:
                    self.board[i][j] = self.MARKED
                    return True
        return False

    def is_winning(self):
        if self.won:
            return True

        is_winning = self.has_winning_row() or self.has_winning_column()

        if is_winning:
            self.won = True

        return self.won

    def has_winning_row(self):
        for i in range(0, self.size):
            marked_row = True
            for j in range(0, self.size):
                if self.board[i][j] != self.MARKED:
                    marked_row = False
                    break
            if marked_row:
                return True

        return False

    def has_winning_column(self):
        for i in range(0, self.size):
            marked_column = True
            for j in range(0, self.size):
                if self.board[j][i] != self.MARKED:
                    marked_column = False
                    break
            if marked_column:
                return True

        return False

    def get_unmarked_sum(self) -> int:
        unmarked_sum = 0
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.board[i][j] != self.MARKED:
                    unmarked_sum += self.board[i][j]

        return unmarked_sum


with open(FILE) as f:
    # read called numbers
    numbers_called = list(map(int, f.readline().strip().split(',')))

    bingos = []

    # while empty line exists
    while f.readline():
        bingo_board = []
        # read bingo
        for _ in range(BINGO_SIZE):
            bingo_board.append(list(map(int, f.readline().strip().split())))

        bingos.append(Bingo(BINGO_SIZE, bingo_board))

    for called_number in numbers_called:
        for bingo in bingos:
            marked = bingo.mark(called_number)
            if marked and bingo.is_winning():
                unmarked_sum = bingo.get_unmarked_sum()
                print("%d * %d = %d" % (unmarked_sum, called_number, unmarked_sum * called_number))
                break
        else:
            continue
        break

# 2. part - play bingo and find who wins the last

with open(FILE) as f:
    # read called numbers
    numbers_called = list(map(int, f.readline().strip().split(',')))

    bingos = []

    # while empty line exists
    while f.readline():
        bingo_board = []
        # read bingo
        for _ in range(BINGO_SIZE):
            bingo_board.append(list(map(int, f.readline().strip().split())))

        bingos.append(Bingo(BINGO_SIZE, bingo_board))

    win_count = 0

    for called_number in numbers_called:
        for bingo in bingos:
            marked = bingo.mark(called_number)
            if marked and bingo.is_winning():
                win_count += 1
                if win_count == len(bingos):
                    unmarked_sum = bingo.get_unmarked_sum()
                    print("%d * %d = %d" % (unmarked_sum, called_number, unmarked_sum * called_number))
