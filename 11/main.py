# https://adventofcode.com/2021/day/11

from collections import deque

FILE = 'input.txt'
# FILE = 'input-small.txt'

SIZE = 10

DIRECTIONS = {
    (1, 1),
    (1, 0),
    (1, -1),
    (0, 1),
    (0, -1),
    (-1, -1),
    (-1, 0),
    (-1, 1),
}

with open(FILE) as f:
    G = []
    for line in f.readlines():
        G.append(list(map(int, list(line.strip()))))

    flash_count = 0
    flashed_count_100 = None
    flashed_all_step = None

    step = 1
    while flashed_count_100 is None or flashed_all_step is None:
        flash = deque()
        flashed = []

        # Find who is going to start flashing
        for i in range(SIZE):
            for j in range(SIZE):
                G[i][j] += 1

                if G[i][j] == 10:
                    flash.append((i, j))

        # Update neighbours of flashed octopuses
        while flash:
            i, j = flash.pop()
            flash_count += 1
            flashed.append((i, j))

            for d in DIRECTIONS:
                new_i = i + d[0]
                new_j = j + d[1]

                if new_i < 0 or new_j < 0 or new_i >= SIZE or new_j >= SIZE:
                    continue

                G[new_i][new_j] += 1

                # Find who is going to start flashing
                if G[new_i][new_j] == 10:
                    flash.append((new_i, new_j))

            # Solve 2. part
            if len(flashed) == SIZE * SIZE:
                flashed_all_step = step

            # Clear counters for flashed octopuses
            for i, j in flashed:
                G[i][j] = 0

        # Solve 1. part
        if step == 100:
            flashed_count_100 = flash_count
        step += 1

    # 1. part
    print(flashed_count_100)

    # 2. part
    print(flashed_all_step)
