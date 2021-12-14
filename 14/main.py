# https://adventofcode.com/2021/day/14

FILE = 'input.txt'
# FILE = 'input-small.txt'

from collections import defaultdict, Counter

# 1. part - naively construct polymer
STEPS = 10

with open(FILE) as f:
    sequence = list(f.readline().strip())
    f.readline()  # empty line

    rules = defaultdict(str)

    while True:
        line = f.readline().strip()
        if not line:
            break

        key, value = line.split(' -> ')
        rules[key] = value

    # Naively construct polymer
    for _ in range(STEPS):
        new_sequence = [sequence[0]]
        for i in range(len(sequence) - 1):
            key = sequence[i] + sequence[i + 1]
            new_sequence.append(rules[key])
            new_sequence.append(sequence[i+1])
        sequence = new_sequence

    c = Counter(sequence)
    most_common = c.most_common()
    print(most_common[0][1] - most_common[-1][1])


# 2. part - memoize partial results
STEPS = 40
RULES = defaultdict(str)

# key: (pair, step), value: Counter
MEMO = {}


def solve(pair: str, step: int) -> Counter:
    if step >= STEPS:
        return Counter()

    key = (pair, step)

    if key in MEMO:
        return MEMO[key]

    middle = RULES[pair]

    c = solve(pair[0] + middle, step + 1) + solve(middle + pair[1], step + 1) + Counter([middle])
    MEMO[key] = c

    return c


with open(FILE) as f:
    sequence = list(f.readline().strip())
    f.readline()  # empty line

    while True:
        line = f.readline().strip()
        if not line:
            break

        key, value = line.split(' -> ')
        RULES[key] = value

    c = Counter(sequence)

    for j in range(len(sequence) - 1):
        subsequence = sequence[j:j + 2]
        c += solve(subsequence[0] + subsequence[1], 0)

    most_common = c.most_common()
    print(most_common[0][1] - most_common[-1][1])
