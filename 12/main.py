# https://adventofcode.com/2021/day/12

from collections import defaultdict

FILE = 'input.txt'
# FILE = 'input-small.txt'

START = 'start'
END = 'end'

with open(FILE) as f:
    G = defaultdict(list)
    for line in f.readlines():
        u, v = line.strip().split('-')
        G[u].append(v)
        G[v].append(u)

    paths = []
    # (current node, path, repeated small cave)
    S = [(START, [START], False)]  # 2. part
    # S = [(START, [START], True)]   # 1. part

    path_count = 0

    # DFS
    while S:
        u, p, rsc = S.pop()

        if u == END:
            path_count += 1
            continue

        # neighbours
        for v in G[u]:
            # skip small caves if repeated
            if v == START or (v.islower() and rsc and v in p):
                continue

            vp = p.copy()
            vp.append(v)
            S.append((v, vp, rsc or (v.islower() and v in p)))

    print(path_count)
