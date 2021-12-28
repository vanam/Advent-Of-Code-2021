# https://adventofcode.com/2021/day/21

FILE = 'input.txt'
# FILE = 'input-small.txt'

# 1. part
END_SCORE = 1000


def deterministic_roll(i):
    iii = 3*i
    return (iii % 100) + 1 + ((iii + 1) % 100) + 1 + ((iii + 2) % 100) + 1


with open(FILE) as f:
    p1 = int(f.readline().strip().split(': ')[1])
    p2 = int(f.readline().strip().split(': ')[1])

    score = [0, 0]
    position = [p1, p2]

    turn = 0
    # players take turns
    while max(score) < END_SCORE:
        p = turn % 2
        position[p] = (position[p] + deterministic_roll(turn) - 1) % 10 + 1
        score[p] += position[p]
        turn += 1

    print(min(score) * (3*turn))

# 2. part
END_SCORE = 21
MEMO = {}


def turn(position, score):
    if (position, score) in MEMO:
        return MEMO[(position, score)]

    result = [0, 0]
    # try all rolls for player 1
    for p1d1 in range(1, 4):
        for p1d2 in range(1, 4):
            for p1d3 in range(1, 4):
                p1roll = p1d1 + p1d2 + p1d3
                p1p = (position[0] + p1roll - 1) % 10 + 1
                p1s = score[0] + p1p

                # check if player 1 wins
                if p1s >= END_SCORE:
                    result[0] += 1
                    continue

                # try all rolls for player 2
                for p2d1 in range(1, 4):
                    for p2d2 in range(1, 4):
                        for p2d3 in range(1, 4):
                            p2roll = p2d1 + p2d2 + p2d3

                            p2p = (position[1] + p2roll - 1) % 10 + 1
                            p2s = score[1] + p2p

                            # check if player 2 wins
                            if p2s >= END_SCORE:
                                result[1] += 1
                                continue
                            else:
                                # next turn
                                tmp_res = turn((p1p, p2p), (p1s, p2s))
                                result[0] += tmp_res[0]
                                result[1] += tmp_res[1]

    MEMO[(position, score)] = tuple(result)

    return result


with open(FILE) as f:
    p1 = int(f.readline().strip().split(': ')[1])
    p2 = int(f.readline().strip().split(': ')[1])

    res = turn((p1, p2), (0, 0))
    print(max(res))

# 2. part - optimized
END_SCORE = 21
MEMO = {}


def turn(p1, p2, s1, s2):
    if (p1, p2, s1, s2) in MEMO:
        return MEMO[(p1, p2, s1, s2)]

    result = [0, 0]
    # try all rolls for player 1
    for p1d1 in range(1, 4):
        for p1d2 in range(1, 4):
            for p1d3 in range(1, 4):
                p1roll = p1d1 + p1d2 + p1d3
                p1p = (p1 + p1roll - 1) % 10 + 1
                p1s = s1 + p1p

                # check if player 1 wins
                if p1s >= END_SCORE:
                    result[0] += 1
                    continue

                # next turn (swap p1 with p2)
                tmp_res = turn(p2, p1p, s2, p1s)
                result[1] += tmp_res[0]
                result[0] += tmp_res[1]

    MEMO[(p1, p2, s1, s2)] = tuple(result)

    return result


with open(FILE) as f:
    p1 = int(f.readline().strip().split(': ')[1])
    p2 = int(f.readline().strip().split(': ')[1])

    res = turn(p1, p2, 0, 0)
    print(max(res))
