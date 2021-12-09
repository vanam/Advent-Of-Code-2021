# https://adventofcode.com/2021/day/2

FILE = 'input.txt'
# FILE = 'input-small.txt'

# 1. part - calculate horizontal position and depth

DIRECTIONS = {
    'forward': (1, 0),
    'down': (0, 1),
    'up': (0, -1)
}

with open(FILE) as f:
    lines = f.readlines()

    # [x, y]
    position = [0, 0]

    for line in lines:
        direction_name, amount = line.split(' ')
        amount = int(amount)
        direction = DIRECTIONS[direction_name]

        position[0] += direction[0] * amount
        position[1] += direction[1] * amount

        # Just make sure we don't fly with submarine
        assert position[0] >= 0
        assert position[1] >= 0

    print("%s : %d" % (str(position), position[0] * position[1]))

# 2. part - calculate horizontal position and depth differently

DIRECTIONS = {
    'forward': (1, 1, 0),
    'down': (0, 0, 1),
    'up': (0, 0, -1)
}

with open(FILE) as f:
    lines = f.readlines()

    # [x, y, aim]
    position = [0, 0, 0]

    for line in lines:
        direction_name, amount = line.split(' ')
        amount = int(amount)
        direction = DIRECTIONS[direction_name]

        position[0] += direction[0] * amount
        position[1] += direction[1] * amount * position[2]
        position[2] += direction[2] * amount

        # Just make sure we don't fly with submarine
        assert position[0] >= 0
        assert position[1] >= 0

    print("%s : %d" % (str(position), position[0] * position[1]))
