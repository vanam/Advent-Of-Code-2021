# https://adventofcode.com/2021/day/7

FILE = 'input.txt'
# FILE = 'input-small.txt'

# Note: fuel calculation could be sped up if there are many duplicates in the input


def fuel(A, x):
    f = 0
    for a in A:
        f += abs(a - x)
    return f


def fuel2(A, x):
    f = 0
    for a in A:
        d = abs(a - x)
        # add aritmetic series sum
        f += (d * (d + 1)) // 2
    return f


with open(FILE) as file:
    line = file.readline().strip()
    A = list(map(int, line.split(',')))

    # 1. part - find minimum of fuel function

    from statistics import median, mean
    # rouding behaves rather strangely https://realpython.com/python-rounding/ but it should not make a difference
    fmedian = round(median(A))
    print(fmedian, fuel(A, fmedian), fuel2(A, fmedian))
    fmean = round(mean(A))
    print(fmean, fuel(A, fmean), fuel2(A, fmean))

    # 2. part - find minimum of more complicated fuel function (but still unimodal)
    for f in [fuel, fuel2]:  # Use both fuel functions
        left = min(A)
        right = max(A)

        # ternary search
        while right >= left:
            left_third = left + (right - left) // 3
            right_third = right - (right - left) // 3

            if f(A, left_third) > f(A, right_third):
                left = left_third + 1
            else:
                right = right_third - 1

        print("Minimum at %d: %d" % (left, f(A, left)))

    # 2. part - using mean
    from math import floor, ceil
    fmean = mean(A)
    fmean_floor = floor(fmean)
    fmean_ceil = ceil(fmean)

    # Select minimum from candidates
    print(min(fuel2(A, fmean_floor), fuel2(A, fmean_ceil)))
