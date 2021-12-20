# https://adventofcode.com/2021/day/20

from copy import deepcopy
from collections import defaultdict

FILE = 'input.txt'
# FILE = 'input-small.txt'

STEPS = [2, 50]  # 1.part, 2. part
PADDING = 2

# Naive solution
with open(FILE) as f:
    lines = f.readlines()
    algorithm = lines[0]
    image = [list(line.strip()) for line in lines[2:]]

    for step in range(max(STEPS)):
        new_image = []
        if step == 0:
            blank = '.'
        else:
            blank = algorithm[0] if step % 2 == 1 else algorithm[511]

        # add blank lines at the beginning
        for __ in range(PADDING):
            new_image.append([blank for _ in range(2 * PADDING + len(image[0]))])

        for row in image:
            new_image.append([blank] * PADDING + row + [blank] * PADDING)

        # add blank lines at the end
        for __ in range(PADDING):
            new_image.append([blank for _ in range(2 * PADDING + len(image[0]))])

        image = new_image
        old_image = deepcopy(image)

        # enhance
        lit_count = 0
        for i in range(PADDING - 1, len(image) - PADDING + 1):
            for j in range(PADDING - 1, len(image[0]) - PADDING + 1):
                number = 0
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        number <<= 1
                        number += 1 if old_image[i + k][j + l] == '#' else 0
                image[i][j] = algorithm[number]
                lit_count += 1 if algorithm[number] == '#' else 0

        # fix padding
        fix = algorithm[0] if blank == '.' else algorithm[511]

        for i in range(len(image[0])):
            image[0][i] = fix
            image[len(image) - 1][i] = fix

        for i in range(len(image)):
            image[i][0] = fix
            image[i][len(image[0]) - 1] = fix

        if step + 1 in STEPS:
            print(lit_count)

# Optimized solution
with open(FILE) as f:
    lines = f.readlines()
    algorithm = lines[0]
    image_lines = lines[2:]
    image_y_dim = len(image_lines)
    image_x_dim = len(image_lines)

    blank = '.'
    image = defaultdict(lambda: '.')
    for y in range(image_y_dim):
        for x in range(image_x_dim):
            image[(x, y)] = image_lines[y][x]

    for step in range(1, max(STEPS) + 1):
        if step == 0:
            blank = '.'
        else:
            blank = algorithm[0] if step % 2 == 0 else algorithm[511]
        new_image = defaultdict(lambda: blank)

        image_x_dim += 2
        image_y_dim += 2

        lit_count = 0
        for y in range(-step, image_y_dim - step):
            for x in range(-step, image_x_dim - step):
                number = 0
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        number <<= 1
                        number += 1 if image[(x + l, y + k)] == '#' else 0
                new_image[(x, y)] = algorithm[number]
                lit_count += 1 if algorithm[number] == '#' else 0

        image = new_image

        if step in STEPS:
            print(lit_count)
