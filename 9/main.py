# https://adventofcode.com/2021/day/9

FILE = 'input.txt'
# FILE = 'input-small.txt'

DIRECTIONS = [[0, 1], [1, 0], [-1, 0], [0, -1]]

# 1. part - find low points
with open(FILE) as f:
    A = []
    for line in f.readlines():
        A.append(line.strip())

    x_dim = len(A[0])
    y_dim = len(A)

    sum_of_low_points = 0

    for y in range(y_dim):
        for x in range(x_dim):
            h = A[y][x]

            low_point = True

            for d in DIRECTIONS:
                new_x = x + d[0]
                new_y = y + d[1]

                if new_x < 0 or new_x >= x_dim or new_y < 0 or new_y >= y_dim:
                    # outside of area
                    continue

                if A[new_y][new_x] <= h:
                    low_point = False
                    break
            if low_point:
                # print("Low ", h)
                sum_of_low_points += 1 + int(h)
    print(sum_of_low_points)

# 2. part - find basins (recursive)
from functools import reduce

FLOODED = 'x'
MAX_HEIGHT = '9'

with open(FILE) as f:
    A = []
    for line in f.readlines():
        A.append(list(line.strip()))

    x_dim = len(A[0])
    y_dim = len(A)

    basin_sizes = []

    def flood_fill(A, x, y):
        flooded = 1

        A[y][x] = FLOODED

        for d in DIRECTIONS:
            new_x = x + d[0]
            new_y = y + d[1]

            if new_x < 0 or new_x >= x_dim or new_y < 0 or new_y >= y_dim:
                # outside of area
                continue

            # Don't flood what is already flooded and max height
            if A[new_y][new_x] not in [FLOODED, MAX_HEIGHT]:
                flooded += flood_fill(A, new_x, new_y)

        return flooded

    for y in range(y_dim):
        for x in range(x_dim):
            h = A[y][x]

            # Start new flooding
            if h not in [FLOODED, MAX_HEIGHT]:
                basin_sizes.append(flood_fill(A, x, y))

    basin_sizes.sort()

    # Multiply 3 bigest basins
    print(reduce((lambda x, y: x * y), basin_sizes[-3:]))

# 2. part - find basins (iterative)
from collections import deque

with open(FILE) as f:
    A = []
    for line in f.readlines():
        A.append(list(line.strip()))

    x_dim = len(A[0])
    y_dim = len(A)

    basin_sizes = []

    def flood_fill(A, x, y):
        flooded = 1

        A[y][x] = FLOODED

        for d in DIRECTIONS:
            new_x = x + d[0]
            new_y = y + d[1]

            if new_x < 0 or new_x >= x_dim or new_y < 0 or new_y >= y_dim:
                # outside of area
                continue

            # Don't flood what is already flooded and max height
            if A[new_y][new_x] not in [FLOODED, MAX_HEIGHT]:
                flooded += flood_fill(A, new_x, new_y)

        return flooded

    for y in range(y_dim):
        for x in range(x_dim):
            # Start new flooding
            if A[y][x] not in [FLOODED, MAX_HEIGHT]:
                flooded = 0
                Q = deque()
                Q.append((x, y))
                while Q:
                    qx, qy = Q.pop()

                    if A[qy][qx] in [FLOODED, MAX_HEIGHT]:
                        continue

                    A[qy][qx] = FLOODED
                    flooded += 1

                    for d in DIRECTIONS:
                        new_x = qx + d[0]
                        new_y = qy + d[1]

                        if new_x < 0 or new_x >= x_dim or new_y < 0 or new_y >= y_dim:
                            # outside of area
                            continue

                        # Don't flood what is already flooded and max height
                        if A[new_y][new_x] in [FLOODED, MAX_HEIGHT]:
                            continue

                        Q.append((new_x, new_y))

                basin_sizes.append(flooded)

    basin_sizes.sort()

    # Multiply 3 bigest basins
    print(reduce((lambda x, y: x * y), basin_sizes[-3:]))