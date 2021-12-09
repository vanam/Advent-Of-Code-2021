# https://adventofcode.com/2021/day/1

import sys

FILE = 'input.txt'
# FILE = 'input-small.txt'

# 1. part - count how many times the value increased
with open(FILE) as f:
    lines = f.readlines()

    last_val = sys.maxsize
    counter = 0

    for line in lines:
        val = int(line)
        if val > last_val:
            counter += 1
        last_val = val

    print(counter)

# 2. part - count how many times the sliding window sum increased
from collections import deque

WINDOW_SIZE = 3

with open(FILE) as f:
    lines = f.readlines()

    window = deque()
    last_window_sum = sys.maxsize
    counter = 0

    for line in lines:
        val = int(line)

        # Put another value to window
        window.append(val)

        # Unless we have complete window
        if len(window) < WINDOW_SIZE:
            continue
        elif len(window) > WINDOW_SIZE:
            # Keep window size
            window.popleft()

        current_window_sum = sum(window)
        if current_window_sum > last_window_sum:
            counter += 1

        last_window_sum = current_window_sum

    print(counter)

# 2. part - count how many times the sliding window sum increased (optimized)
WINDOW_SIZE = 3

with open(FILE) as f:
    lines = f.readlines()

    window = [None] * WINDOW_SIZE
    counter = 0

    for i, line in enumerate(lines):
        val = int(line)

        # Pointer to oldest element in window
        p = i % WINDOW_SIZE

        # Increment counter if the oldest element is less than new value
        if window[p] is not None and window[p] < val:
            counter += 1

        window[p] = val

    print(counter)
