# https://adventofcode.com/2021/day/13

FILE = 'input.txt'
# FILE = 'input-small.txt'

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

        if line == '':
            break

        instruction_count += 1
        fold, fold_position = line[11:].split('=')
        fold_position = int(fold_position)

        new_dots = set()
        if fold == 'x':
            for x, y in dots:
                if x < fold_position:
                    new_dots.add((x, y))
                else:
                    new_dots.add((x - 2 * (x - fold_position), y))
        elif fold == 'y':
            for x, y in dots:
                if y < fold_position:
                    new_dots.add((x, y))
                else:
                    new_dots.add((x, y - 2 * (y - fold_position)))

        dots = new_dots

        if instruction_count == 1:
            print(len(dots))  # 1. part

    # visualize 2. part
    for i in range(10):
        for j in range(50):
            if (j, i) in dots:
                print('█', end='')
            else:
                print('░', end='')
        print("")
