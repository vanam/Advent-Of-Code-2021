# https://adventofcode.com/2021/day/10

from collections import deque

FILE = 'input.txt'
# FILE = 'input-small.txt'

BRACKETS = {
    '(': ')',
    '[': ']',
    '<': '>',
    '{': '}',
}

ERROR_SCORE = {
    ')': 3,
    ']': 57,
    '>': 25137,
    '}': 1197,
}

INCOMPLETE_SCORE = {
    '(': 1,
    '[': 2,
    '<': 4,
    '{': 3,
}

with open(FILE) as f:
    syntax_error_score = 0
    incomplete_scores = []

    for line in f.readlines():
        line = line.strip()

        S = deque()

        for bracket in line:
            if bracket in BRACKETS.keys():
                S.append(bracket)
            else:
                # Cannot close if there is nothing to close
                if not S:
                    assert False  # does not happen

                opening_bracket = S.pop()

                if BRACKETS[opening_bracket] != bracket:
                    syntax_error_score += ERROR_SCORE[bracket]
                    break

        else:  # Process only incomplete lines
            if S:
                incomplete_score = 0
                while S:
                    incomplete_score *= 5
                    incomplete_score += INCOMPLETE_SCORE[S.pop()]
                incomplete_scores.append(incomplete_score)

    # 1. part
    print(syntax_error_score)

    # 2. part
    incomplete_scores.sort()
    print(incomplete_scores[len(incomplete_scores) // 2])
