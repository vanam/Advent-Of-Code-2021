# https://adventofcode.com/2021/day/8

FILE = 'input.txt'
# FILE = 'input-small.txt'
# FILE = 'input-smallest.txt'

# 1. part
with open(FILE) as f:
    # Number of segments for numbers 1, 7, 4, 8
    unique_number_lenghts = [2, 3, 4, 7]

    coutner = 0

    for line in f.readlines():
        patterns, output = line.strip().split(' | ')
        # ignore patterns for now
        output = output.split()

        for p in output:
            if len(p) in unique_number_lenghts:
                coutner += 1

    print(coutner)

# 2. part - find correct mapping (combinatorics)

import re
import itertools

PATTERN_2_DIGIT = {
    'abcefg': 0,
    'cf': 1,  # unique
    'acdeg': 2,
    'acdfg': 3,
    'bcdf': 4,  # unique
    'abdfg': 5,
    'abdefg': 6,
    'acf': 7,  # unique
    'abcdefg': 8,  # unique
    'abcdfg': 9
}


def map_number(mapping: dict, pattern: str):
    new_pattern = ''
    for s in pattern:
        new_pattern += mapping.get(s)

    # sort
    new_pattern = "".join(sorted(list(new_pattern)))

    if new_pattern not in PATTERN_2_DIGIT.keys():
        return -1

    return PATTERN_2_DIGIT.get(new_pattern)


def find_mapping(patterns: list):
    # find unique patterns
    up = []
    for p in patterns:
        if len(p) in unique_number_lenghts:
            up.append(p)

    # unique patterns for numbers 1, 7, 4, 8
    up = sorted(up, key=len)

    # wrong segments for known numbers
    n1 = list(up[0])
    n7 = list(re.sub("[" + up[0] + "]", '', up[1]))
    n4 = list(re.sub("[" + up[0] + up[1] + "]", '', up[2]))
    n8 = list(re.sub("[" + up[0] + up[1] + up[2] + "]", '', up[3]))

    # possible segment mappings
    M = {
        # number 1
        n1[0]: ['c', 'f'],
        n1[1]: ['c', 'f'],
        # number 7
        n7[0]: ['a'],
        # number 4
        n4[0]: ['b', 'd'],
        n4[1]: ['b', 'd'],
        # number 8
        n8[0]: ['e', 'g'],
        n8[1]: ['e', 'g'],
    }

    # generate all possible permutations
    keys, values = zip(*M.items())
    possible_mappings = [dict(zip(keys, v)) for v in itertools.product(*values)]

    # filter out mapping with repeating values
    possible_mappings = filter(lambda d: len(set(d.values())) == 7, possible_mappings)  # There are only 9 of them

    # try if we can successfully map numbers
    for mapping in possible_mappings:
        for p in patterns:
            if map_number(mapping, p) == -1:
                break
        else:
            return mapping

    assert False  # Should not happen


with open(FILE) as f:
    # Number of segments for numbers 1, 7, 4, 8
    unique_number_lenghts = [2, 3, 4, 7]

    sum_of_all_output_values = 0

    for line in f.readlines():
        patterns, output = line.strip().split(' | ')
        patterns = patterns.split()
        output = output.split()

        # sort patterns/output
        patterns = ["".join(sorted(list(p))) for p in patterns]
        output = ["".join(sorted(list(o))) for o in output]

        # find correct mapping
        mapping = find_mapping(patterns)

        output_number = 0
        for o in output:
            oo = map_number(mapping, o)
            output_number *= 10
            output_number += oo

        sum_of_all_output_values += output_number
    print(sum_of_all_output_values)

# 2. part - find correct mapping (with frequency table there is only one solution)

# create frequency table from correct mapping
CORRECT_FT = {}
for p in PATTERN_2_DIGIT.keys():
    for s in p:
        CORRECT_FT[s] = CORRECT_FT.get(s, 0) + 1


def find_mapping2(patterns):
    # create frequency table from wrong mapping
    ft = {}
    for p in patterns:
        for s in p:
            ft[s] = ft.get(s, 0) + 1

    reversed_ft = dict(map(reversed, ft.items()))

    # discover correct mapping for segments with unique frequency
    M = {
        reversed_ft[6]: 'b',
        reversed_ft[4]: 'e',
        reversed_ft[9]: 'f',
    }

    # Number of segments for numbers 1, 7, 4, 8
    unique_number_lenghts = [2, 3, 4, 7]

    # find unique patterns
    up = []
    for p in patterns:
        if len(p) in unique_number_lenghts:
            up.append(list(p))

    # unique patterns for numbers 1, 7, 4, 8
    up = sorted(up, key=len)

    # wrong segments for known numbers
    M[list(filter(lambda s: s not in M.keys(), up[0]))[0]] = 'c'  # from 1
    M[list(filter(lambda s: s not in M.keys(), up[1]))[0]] = 'a'  # from 7
    M[list(filter(lambda s: s not in M.keys(), up[2]))[0]] = 'd'  # from 4
    M[list(filter(lambda s: s not in M.keys(), up[3]))[0]] = 'g'  # from 8

    return M


with open(FILE) as f:
    # Number of segments for numbers 1, 7, 4, 8
    unique_number_lenghts = [2, 3, 4, 7]

    sum_of_all_output_values = 0

    for line in f.readlines():
        patterns, output = line.strip().split(' | ')
        patterns = patterns.split()
        output = output.split()

        # sort patterns/output
        patterns = ["".join(sorted(list(p))) for p in patterns]
        output = ["".join(sorted(list(o))) for o in output]

        # find correct mapping
        mapping = find_mapping2(patterns)

        output_number = 0
        for o in output:
            oo = map_number(mapping, o)
            output_number *= 10
            output_number += oo

        sum_of_all_output_values += output_number
    print(sum_of_all_output_values)