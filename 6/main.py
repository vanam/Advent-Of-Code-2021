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

