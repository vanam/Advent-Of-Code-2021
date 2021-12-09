# https://adventofcode.com/2021/day/3

INPUT_LENGTH = 12
FILE = 'input.txt'
# INPUT_LENGTH = 5
# FILE = 'input-small.txt'

# 1. part - calculate power consumption

with open(FILE) as f:
    lines = f.readlines()

    # find most common bit in the corresponding position
    bits = {}  # don't want to store whole input in array

    for line in lines:
        line = line.strip()  # remove new line at the end

        for i, b in enumerate(line):
            b = int(b)

            # get counter at position i
            b_counter = bits.get(i, [0, 0])
            # update count
            b_counter[b] += 1
            bits[i] = b_counter

    number_len = len(bits)

    # most common bit in the corresponding position of all numbers
    gama_rate = 0

    # least common bit in the corresponding position of all numbers
    epsilon_rate = 0

    for i in range(number_len):
        # shift left
        gama_rate <<= 1
        epsilon_rate <<= 1

        # add 1 to correct number
        b_counter = bits.get(i)
        if b_counter[0] > b_counter[1]:
            epsilon_rate += 1
        else:
            gama_rate += 1

    print("%d * %d = %d" % (gama_rate, epsilon_rate, gama_rate * epsilon_rate))

# 2. part - calculate life support rating


class Node:
    def __init__(self, value: int):
        self.b_counter = [0, 0]
        self.value = value
        self.left = None
        self.right = None

    def add_node(self, value: int) -> 'Node':
        self.b_counter[value] += 1

        if value == 0 and self.left is None:
            self.left = Node(0)
        elif value == 1 and self.right is None:
            self.right = Node(1)

        return self.left if value == 0 else self.right

    def is_last(self) -> bool:
        return self.left == self.right is None

    def __str__(self) -> str:
        return "%d %s" % (self.value, self.b_counter)


with open(FILE) as f:
    lines = f.readlines()

    # build binary tree from numbers
    root = Node(-1)

    for line in lines:
        line = line.strip()  # remove new line at the end

        current_node = root

        for b in line:
            b = int(b)
            current_node = current_node.add_node(b)

    # lookup oxygen generator number
    oxygen_generator_number = 0
    current_node = root

    while not current_node.is_last():
        b_counter = current_node.b_counter
        oxygen_generator_number <<= 1

        if b_counter[1] >= b_counter[0]:
            # one
            oxygen_generator_number += 1
            current_node = current_node.right
        else:
            # zero
            current_node = current_node.left

    # lookup CO2 scrubber rating
    co2_scrubber_rating = 0
    current_node = root

    while not current_node.is_last():
        b_counter = current_node.b_counter
        co2_scrubber_rating <<= 1

        if b_counter[0] == 0:
            # one
            co2_scrubber_rating += 1
            current_node = current_node.right
        elif b_counter[1] == 0:
            # zero
            current_node = current_node.left
        elif b_counter[0] <= b_counter[1]:
            # zero
            current_node = current_node.left
        else:
            # one
            co2_scrubber_rating += 1
            current_node = current_node.right

    print("%d * %d = %d" % (oxygen_generator_number, co2_scrubber_rating, oxygen_generator_number * co2_scrubber_rating))

# 1. part - calculate power consumption (optimized)

with open(FILE) as f:
    lines = f.readlines()
    counts = [0 for _ in range(2 * INPUT_LENGTH)]

    for line in lines:
        line = line.strip()  # remove new line at the end

        current_node = root

        for i, b in enumerate(line):
            b = int(b)
            counts[2 * i + b] += 1

    # most common bit in the corresponding position of all numbers
    gama_rate = 0

    # least common bit in the corresponding position of all numbers
    epsilon_rate = 0

    for i in range(INPUT_LENGTH):
        # shift left
        gama_rate <<= 1
        epsilon_rate <<= 1

        if counts[2 * i] > counts[2 * i + 1]:
            epsilon_rate += 1
        else:
            gama_rate += 1

    print("%d * %d = %d" % (gama_rate, epsilon_rate, gama_rate * epsilon_rate))

# 2. part - calculate life support rating (optimized)

with open(FILE) as f:
    lines = f.readlines()
    tree = [0 for _ in range(1 << (INPUT_LENGTH + 1))]

    for line in lines:
        line = line.strip()  # remove new line at the end
        number = int('1' + line, 2)  # add 1 at the beginning - root

        for _ in range(INPUT_LENGTH):
            tree[number] += 1
            number >>= 1

    # oxygen generator number
    oxygen_generator_number = 1

    # CO2 scrubber rating
    co2_scrubber_rating = 1

    for _ in range(INPUT_LENGTH):
        oxygen_generator_number <<= 1
        co2_scrubber_rating <<= 1

        if tree[oxygen_generator_number + 1] >= tree[oxygen_generator_number]:
            oxygen_generator_number += 1

        if tree[co2_scrubber_rating] == 0 or (tree[co2_scrubber_rating] > tree[co2_scrubber_rating + 1] != 0):
            co2_scrubber_rating += 1

    # remove 1 at the beginning - root
    oxygen_generator_number &= ~(1 << INPUT_LENGTH)
    co2_scrubber_rating &= ~(1 << INPUT_LENGTH)

    print("%d * %d = %d" % (oxygen_generator_number, co2_scrubber_rating, oxygen_generator_number * co2_scrubber_rating))
