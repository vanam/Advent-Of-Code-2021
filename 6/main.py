# https://adventofcode.com/2021/day/6

FILE = 'input.txt'
FILE = 'input-small.txt'

# Simulate lanternfish growth

# length of simulation
DAYS = 80   # 1. part
DAYS = 256  # 2. part

with open(FILE) as f:
    init_state = list(map(int, (f.readline().split(','))))  # list of lanternfish

    # Keep count of lanternfish in certain state
    state = [0 for _ in range(0, 9)]

    for lf in init_state:
        state[lf] += 1

    # keep index where 0
    p = 0
    for _ in range(DAYS):
        count0 = state[p]

        # a 0 breeds a 6
        state[(p + 7) % 9] += count0
        # a 0 becomes a 8

        p += 1
        p %= 9

    print(sum(state))

# O(logN) solution with matrix exponentiation


class Mat:
    def __init__(self, size: int):
        self.size = size
        self.m = [[0 for _ in range(size)] for _ in range(size)]

    def __getitem__(self, item):
        return self.m[item]

    def __mul__(self, other: 'Mat'):
        ans = Mat(self.size)
        for i in range(self.size):
            for j in range(self.size):
                for k in range(self.size):
                    ans[i][j] += self.m[i][k] * other.m[k][j]

        return ans

    def __str__(self):
        rows = []
        for r in range(self.size):
            rows.append(str(self.m[r]))
        return '[' + ",\n".join(rows) + ']'

    @staticmethod
    def pow(m: 'Mat', n: int):
        ans = Mat(m.size)
        for i in range(m.size):
            ans[i][i] = 1
        while n:
            if n & 1:
                ans *= m
            m *= m
            n //= 2
        return ans


with open(FILE) as f:
    init_state = list(map(int, (f.readline().split(','))))  # list of lanternfish

    # Keep count of lanternfish in certain state
    state = [0 for _ in range(0, 9)]

    for lf in init_state:
        state[lf] += 1

    M = Mat(9)
    # Decrease the number of days until it creates a new lanternfish
    for i in range(8):
        M[i][i + 1] = 1
    M[6][0] = 1  # reset internal timer
    M[8][0] = 1  # create a new lanternfish

    M = Mat.pow(M, DAYS)

    ans = 0
    for i in range(9):
        for j in range(9):
            ans += M[i][j] * state[j]
    print(ans)

