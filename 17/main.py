# https://adventofcode.com/2021/day/17

import re

FILE = 'input.txt'
# FILE = 'input-small.txt'

# Brute force approach

START = (0, 0)
TARGET = None


def trajectory(vx, vy):
    x, y = START

    max_y = y  # max y at trajectory

    while x <= TARGET[1] and y >= TARGET[2]:
        x += vx
        y += vy

        max_y = max(max_y, y)

        vx = vx - 1 if vx > 1 else 0
        vy -= 1

        if TARGET[0] <= x <= TARGET[1] and TARGET[2] <= y <= TARGET[3]:
            # Hit
            return max_y

    return None


with open(FILE) as f:
    target_parts = list(filter(lambda s: s != '', re.split('[xy=, ]', f.readline()[13:])))
    tx1, tx2 = list(map(int, target_parts[0].split('..')))
    ty1, ty2 = list(map(int, target_parts[1].split('..')))
    TARGET = (tx1, tx2, ty1, ty2)

    # min vx - must reach tartget's x1 (aritmetic sum) (d * (d + 1)) // 2
    min_vx = 0
    s = 0
    while s < TARGET[0]:
        min_vx += 1
        s += min_vx

    # max vx - overshoot tartget's x2 in one step
    max_vx = TARGET[1] + 1
    # min vy - overshoot tartget's y2 in one step
    min_vy = TARGET[2] - 1
    # max vy ?? - 100 seems good
    max_vy = 100

    max_y = 0                   # max y among all trajectories
    hit_trajectory_counter = 0  # number of trajectories which hit target area
    for vx in range(min_vx, max_vx):
        vy = min_vy
        for vy in range(min_vy, max_vy):
            tmp_max_y = trajectory(vx, vy)

            if tmp_max_y is not None:
                hit_trajectory_counter += 1
                max_y = max(tmp_max_y, max_y)

    print(max_y)
    print(hit_trajectory_counter)

# Sane approach

with open(FILE) as f:
    target_parts = list(filter(lambda s: s != '', re.split('[xy=, ]', f.readline()[13:])))
    tx1, tx2 = list(map(int, target_parts[0].split('..')))
    ty1, ty2 = list(map(int, target_parts[1].split('..')))
    TARGET = (tx1, tx2, ty1, ty2)

    # No need to worry about x because the best height
    # is the same for any vx value ending up stabilizing
    # the probe in target xrange.
    #
    # Best height is vy * (vy + 1) / 2 so we need to max
    # vy. As the probe always comes back to y = 0, its
    # first depth is -(vy + 1) that is limited by target
    # low bound.
    max_vy = -ty1 - 1
    max_y = (1 + max_vy) * max_vy // 2  # arithmetic sum from the start to the top: vy + (vy-1) + (vy-2) + .... 1
    print(max_y)  # 1. part

    # Try all possible velocities

    # min vx - must reach tartget's x1 (aritmetic sum) (d * (d + 1)) // 2
    min_vx = 0
    s = 0
    while s < TARGET[0]:
        min_vx += 1
        s += min_vx
    # max vx - overshoot tartget's x2 in one step
    max_vx = TARGET[1]
    # min vy - overshoot tartget's y2 in one step
    min_vy = TARGET[2]
    # max vy - solution from 1. part
    max_vy = max_vy

    hit_trajectory_counter = 0  # number of trajectories which hit target area
    for vx in range(min_vx, max_vx + 1):
        vy = min_vy
        for vy in range(min_vy, max_vy + 1):
            tmp_max_y = trajectory(vx, vy)

            if tmp_max_y is not None:
                hit_trajectory_counter += 1

    print(hit_trajectory_counter)  # 2. part
