# https://adventofcode.com/2021/day/13

FILE = 'input.txt'
# FILE = 'input-small.txt'

START = 'start'
END = 'end'

with open(FILE) as f:
    # read dots
    dots = set()
    while True:
        line = f.readline().strip()

        if line.strip() == '':
            break

        x, y = list(map(int, line.split(',')))
        dots.add((x, y))

    # read and follow instructions
    instruction_count = 0
    while True:
        line = f.readline().strip()

        if line.strip() == '':
            break

        instruction_count += 1
        fold, pos = line[11:].split('=')
        pos = int(pos)

        if fold == 'x':
            new_dots = set()
            for x, y in dots:
                if x < pos:
                    new_dots.add((x, y))
                else:
                    new_dots.add((x - 2 * (x - pos), y))

            dots = new_dots
        elif fold == 'y':
            new_dots = set()
            for x, y in dots:
                if y < pos:
                    new_dots.add((x, y))
                else:
                    new_dots.add((x, y - 2 * (y - pos)))

            dots = new_dots
        else:
            assert False  # should not happen

        if instruction_count == 1:
            print(len(dots))  # 1. part

    # visualize 2. part and read it
    for i in range(10):
        for j in range(50):
            if (j, i) in dots:
                print('#', end='')
            else:
                print('.', end='')
        print("")






