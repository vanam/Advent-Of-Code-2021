# https://adventofcode.com/2021/day/25

FILE = 'input.txt'
# FILE = 'input-small.txt'

SOUTH = 'v'
EAST = '>'
EMPTY = '.'

MOVE_EAST = (1, 0)
MOVE_SOUTH = (0, 1)


def print_map(east: set, south: set, max_x: int, max_y: int):
    for y in range(max_y):
        for x in range(max_x):
            position = (x, y)
            if position in east:
                print(EAST, end="")
            elif position in south:
                print(SOUTH, end="")
            else:
                print(EMPTY, end="")
        print("")


with open(FILE) as f:
    east = set()
    south = set()

    lines = [line.strip() for line in f.readlines()]

    max_y = len(lines)
    max_x = len(lines[0])
    for y in range(max_y):
        line = lines[y]
        for x in range(max_x):
            c = line[x]
            if c == EAST:
                east.add((x, y))
            elif c == SOUTH:
                south.add((x, y))

    step = 1
    moved = True
    while moved:
        step += 1
        moved = False

        new_east = set()
        for e in east:
            new_e = ((e[0] + MOVE_EAST[0]) % max_x, e[1] + MOVE_EAST[1])
            if new_e in east or new_e in south:
                new_east.add(e)  # no move
                continue
            moved = True
            new_east.add(new_e)
        east = new_east

        new_south = set()
        for s in south:
            new_s = (s[0] + MOVE_SOUTH[0], (s[1] + MOVE_SOUTH[1]) % max_y)
            if new_s in east or new_s in south:
                new_south.add(s)  # no move
                continue
            moved = True
            new_south.add(new_s)
        south = new_south

    print(step - 1)
