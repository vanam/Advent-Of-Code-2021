# https://adventofcode.com/2021/day/15

from collections import defaultdict
from queue import PriorityQueue

FILE = 'input.txt'
# FILE = 'input-small.txt'

# 1. part - Find shortest path (Dijkstra)
G = []
D = []
DIRECTIONS = [(0, 1), (0, -1), (-1, 0), (1, 0)]
INF = 10000000000

with open(FILE) as f:
    for line in f.readlines():
        row = list(map(int, list(line.strip())))

        G.append(row)
        D.append([INF for _ in range(len(row))])

    max_y = len(G)
    max_x = len(G[0])

    start = (0, 0)
    D[0][0] = 0
    end = (max_x - 1, max_x - 1)

    Q = PriorityQueue()
    Q.put((D[0][0], start))

    lowest_total_risk = None

    while not Q.empty():
        risk, u = Q.get()
        ux, uy = u

        if u == end:
            lowest_total_risk = risk
            break

        if risk > D[uy][ux]:
            continue

        for d in DIRECTIONS:
            vx = ux + d[0]
            vy = uy + d[1]

            if vx < 0 or vx >= max_x or vy < 0 or vy >= max_y:
                continue

            if D[uy][ux] + G[vy][vx] < D[vy][vx]:
                D[vy][vx] = D[uy][ux] + G[vy][vx]
                Q.put((D[vy][vx], (vx, vy)))

    print(lowest_total_risk)


# 2. part - Find shortest path (Dijkstra) at extended map (calculated on the fly)
G = []
DIRECTIONS = [(0, 1), (0, -1), (-1, 0), (1, 0)]
INF = 10000000000
SCALE = 5


def graph(x: int, y: int):
    sx = x // max_x
    sy = y // max_y

    i = y % max_y
    j = x % max_x

    return (G[i][j] - 1 + sx + sy) % 9 + 1


with open(FILE) as f:
    # read map
    for line in f.readlines():
        row = list(map(int, list(line.strip())))
        G.append(row)

    max_y = len(G)
    max_x = len(G[0])

    start = (0, 0)
    end = (SCALE * max_x - 1, SCALE * max_x - 1)

    distance = defaultdict(lambda: INF)
    distance[start] = 0

    Q = PriorityQueue()
    Q.put((distance[start], start))
    lowest_total_risk = None

    while not Q.empty():
        risk, u = Q.get()
        ux, uy = u

        if u == end:
            lowest_total_risk = risk
            break

        if risk > distance[u]:
            continue

        for d in DIRECTIONS:
            vx = ux + d[0]
            vy = uy + d[1]
            v = (vx, vy)

            if vx < 0 or vx >= SCALE * max_x or vy < 0 or vy >= SCALE * max_y:
                continue

            if distance[u] + graph(vx, vy) < distance[v]:
                distance[v] = distance[u] + graph(vx, vy)
                Q.put((distance[v], v))

    print(lowest_total_risk)
