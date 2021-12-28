import re
from collections import defaultdict

FILE = 'input.txt'
f = open(FILE)
instructions = [line.split() for line in f.readlines()]
f.close()


# ALU simulation
def is_int(s: str):
    return re.match("[-+]?\d+$", s) is not None


def alu(instructions: list, number: str):
    # implicitly init variables with 0
    variables = defaultdict(int)

    # start reading with first digit of number
    d = 0

    for ins in instructions:
        if ins[0] == "inp":
            # read single digit from number
            variables[ins[1]] = int(number[d])
            d += 1
        elif ins[0] == "add":
            val = int(ins[2]) if is_int(ins[2]) else variables[ins[2]]
            variables[ins[1]] = variables[ins[1]] + val
        elif ins[0] == "mul":
            val = int(ins[2]) if is_int(ins[2]) else variables[ins[2]]
            variables[ins[1]] = variables[ins[1]] * val
        elif ins[0] == "div":
            val = int(ins[2]) if is_int(ins[2]) else variables[ins[2]]
            variables[ins[1]] = variables[ins[1]] // val
        elif ins[0] == "mod":
            val = int(ins[2]) if is_int(ins[2]) else variables[ins[2]]
            variables[ins[1]] = variables[ins[1]] % val
        elif ins[0] == "eql":
            val = int(ins[2]) if is_int(ins[2]) else variables[ins[2]]
            variables[ins[1]] = int(variables[ins[1]] == val)
        else:
            # should not happen
            assert False

    return variables


def is_valid(instructions: list, number: str):
    return alu(instructions, number)['z'] == 0

# print(is_valid(instructions, "13579246899999"))


# Reverse engineered MONAD program
CONSTANTS = []
for i in range(14):
    offset = i * 18
    A = int(instructions[4 + offset][2])
    B = int(instructions[5 + offset][2])
    C = int(instructions[15 + offset][2])
    CONSTANTS.append((A, B, C))


# CONSTANTS = [
#     (1, 14, 14),    # 1
#     (1, 14, 2),     # 2
#     (1, 14, 1),     # 3
#     (1, 12, 13),    # 4
#     (1, 15, 5),     # 5
#     (26, -12, 5),   # 6
#     (26, -12, 5),   # 7
#     (1, 12, 9),     # 8
#     (26, -7, 3),    # 9
#     (1, 13, 13),    # 10
#     (26, -8, 2),    # 11
#     (26, -5, 1),    # 12
#     (26, -10, 11),  # 13
#     (26, -7, 8),    # 14
# ]


def is_valid(num: list):
    z = 0
    for i, w in enumerate(num):
        A, B, C = CONSTANTS[i]

        if (z % 26 + B) == w:
            z //= A
        else:
            z = (z // A) * 26 + w + C

        # one-liner
        # z = (0 if (z % 26 + B) == w else 1) * ((z // A) * 25 + w + C) + (z // A)
    return z == 0


# number = [int(c) for c in "13579246899999"]
# print(is_valid(number))

# Problem solution
data = {14: {0: []}}  # start with z=0 at the end
for i in reversed(range(0, 14)):  # 13, 12, ..., 0
    i_data = defaultdict(list)
    A, B, C = CONSTANTS[i]  # constants from my input
    for w in reversed(range(1, 10)):  # try all digits
        for z in data[i + 1].keys():  # look at all z from previous step
            for a in range(0, A):  # compensate for lost information during division
                # try solution where (z % 26 + B) == w
                pz = z * A + a
                if (pz % 26 + B) == w:
                    assert pz // A == z
                    i_data[pz].append((w, z))

                # try solution where (z % 26 + B) != w
                pz = (z - w - C) // 26 * A + a
                if (pz % 26 + B) != w:
                    if (pz // A) * 26 + w + C == z:  # apparently it also produces invalid solutions
                        i_data[pz].append((w, z))

    data[i] = i_data

zl = 0
zs = 0
largest_number = []
smallest_number = []
for i in range(14):
    wl, zl = data[i][zl][0]
    ws, zs = data[i][zs][-1]

    largest_number.append(str(wl))
    smallest_number.append(str(ws))
print("".join(largest_number))   # 1. part
print("".join(smallest_number))  # 2. part
