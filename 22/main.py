# https://adventofcode.com/2021/day/22

import re
from collections import defaultdict

from typing import List, Union

FILE = 'input.txt'
# FILE = 'input-small.txt'

# 1. part - Brute force
CORE = 50

with open(FILE) as f:
    steps = []
    for line in f.readlines():
        lp = re.split("[=,.]", line.strip())
        steps.append((True if "on" == lp[0][:2] else False, int(lp[1]), int(lp[3]), int(lp[5]), int(lp[7]), int(lp[9]),
                      int(lp[11])))

    reactor = defaultdict(bool)

    for action, x1, x2, y1, y2, z1, z2 in steps:

        if max(x1, x2, y1, y2, z1, z2) > CORE or min(x1, x2, y1, y2, z1, z2) < -CORE:
            continue

        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    reactor[(x, y, z)] = action

    counter = 0
    for key, value in reactor.items():
        if value:
            counter += 1

    print(counter)


# 2. part - Inclusion–exclusion principle (https://en.wikipedia.org/wiki/Inclusion%E2%80%93exclusion_principle)
class Cube:

    def __init__(self, x1, x2, y1, y2, z1, z2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2

    def intersect(self, other: 'Cube') -> Union['Cube', None]:
        x1 = max(self.x1, other.x1)
        x2 = min(self.x2, other.x2)

        y1 = max(self.y1, other.y1)
        y2 = min(self.y2, other.y2)

        z1 = max(self.z1, other.z1)
        z2 = min(self.z2, other.z2)

        # there is overlap between intervals
        if x1 <= x2 and y1 <= y2 and z1 <= z2:
            return Cube(x1, x2, y1, y2, z1, z2)

        # no intersection
        return None

    def difference(self, other: 'Cube') -> List['Cube']:
        intersection = self.intersect(other)

        if intersection is None:
            return []

        # creating 27 tiny cubes is slow
        # subcubes = [
        #     Cube(self.x1, intersection.x1 - 1, self.y1, intersection.y1 - 1, self.z1, intersection.z1 - 1),            # bottom left
        #     Cube(intersection.x1, intersection.x2, self.y1, intersection.y1 - 1, self.z1, intersection.z1 - 1),        # bottom middle
        #     Cube(intersection.x2 + 1, self.x2, self.y1, intersection.y1 - 1, self.z1, intersection.z1 - 1),            # bottom right
        #     Cube(self.x1, intersection.x1 - 1, intersection.y1, intersection.y2, self.z1, intersection.z1 - 1),        # middle left
        #     Cube(intersection.x1, intersection.x2, intersection.y1, intersection.y2, self.z1, intersection.z1 - 1),    # middle middle
        #     Cube(intersection.x2 + 1, self.x2, intersection.y1, intersection.y2, self.z1, intersection.z1 - 1),        # middle right
        #     Cube(self.x1, intersection.x1 - 1, intersection.y2 + 1, self.y2, self.z1, intersection.z1 - 1),            # top left
        #     Cube(intersection.x1, intersection.x2, intersection.y2 + 1, self.y2, self.z1, intersection.z1 - 1),        # top middle
        #     Cube(intersection.x2 + 1, self.x2, intersection.y2 + 1, self.y2, self.z1, intersection.z1 - 1),            # top right
        #
        #     Cube(self.x1, intersection.x1 - 1, self.y1, intersection.y1 - 1, intersection.z1, intersection.z2),        # bottom left
        #     Cube(intersection.x1, intersection.x2, self.y1, intersection.y1 - 1, intersection.z1, intersection.z2),    # bottom middle
        #     Cube(intersection.x2 + 1, self.x2, self.y1, intersection.y1 - 1, intersection.z1, intersection.z2),        # bottom right
        #     Cube(self.x1, intersection.x1 - 1, intersection.y1, intersection.y2, intersection.z1, intersection.z2),    # middle left
        #     # Cube(intersection.x1, intersection.x2, intersection.y1, intersection.y2, intersection.z1, intersection.z2),      # middle middle = intersection -> ignore
        #     Cube(intersection.x2 + 1, self.x2, intersection.y1, intersection.y2, intersection.z1, intersection.z2),    # middle right
        #     Cube(self.x1, intersection.x1 - 1, intersection.y2 + 1, self.y2, intersection.z1, intersection.z2),        # top left
        #     Cube(intersection.x1, intersection.x2, intersection.y2 + 1, self.y2, intersection.z1, intersection.z2),    # top middle
        #     Cube(intersection.x2 + 1, self.x2, intersection.y2 + 1, self.y2, intersection.z1, intersection.z2),        # top right
        #
        #     Cube(self.x1, intersection.x1 - 1, self.y1, intersection.y1 - 1, intersection.z2 + 1, self.z2),            # bottom left
        #     Cube(intersection.x1, intersection.x2, self.y1, intersection.y1 - 1, intersection.z2 + 1, self.z2),        # bottom middle
        #     Cube(intersection.x2 + 1, self.x2, self.y1, intersection.y1 - 1, intersection.z2 + 1, self.z2),            # bottom right
        #     Cube(self.x1, intersection.x1 - 1, intersection.y1, intersection.y2, intersection.z2 + 1, self.z2),        # middle left
        #     Cube(intersection.x1, intersection.x2, intersection.y1, intersection.y2, intersection.z2 + 1, self.z2),    # middle middle
        #     Cube(intersection.x2 + 1, self.x2, intersection.y1, intersection.y2, intersection.z2 + 1, self.z2),        # middle right
        #     Cube(self.x1, intersection.x1 - 1, intersection.y2 + 1, self.y2, intersection.z2 + 1, self.z2),            # top left
        #     Cube(intersection.x1, intersection.x2, intersection.y2 + 1, self.y2, intersection.z2 + 1, self.z2),        # top middle
        #     Cube(intersection.x2 + 1, self.x2, intersection.y2 + 1, self.y2, intersection.z2 + 1, self.z2),            # top right
        # ]

        # create 6 cubes instead
        subcubes = [
            Cube(self.x1, intersection.x1 - 1, self.y1, self.y2, self.z1, self.z2),                                  # left side
            Cube(intersection.x2 + 1, self.x2, self.y1, self.y2, self.z1, self.z2),                                  # right side
            Cube(intersection.x1, intersection.x2, self.y1, intersection.y1 - 1, self.z1, self.z2),                  # bottom middle
            Cube(intersection.x1, intersection.x2, intersection.y2 + 1, self.y2, self.z1, self.z2),                  # top middle
            Cube(intersection.x1, intersection.x2, intersection.y1, intersection.y2, self.z1, intersection.z1 - 1),  # front center
            Cube(intersection.x1, intersection.x2, intersection.y1, intersection.y2, intersection.z2 + 1, self.z2),  # back center
        ]

        return list(filter(lambda c: c.volume() > 0, subcubes))

    def volume(self):
        return (self.x2 - self.x1 + 1) * (self.y2 - self.y1 + 1) * (self.z2 - self.z1 + 1)

    def __eq__(self, other: 'Cube') -> bool:
        return (self.x1, self.x2, self.y1, self.y2, self.z1, self.y2) == (other.x1, other.x2, other.y1, other.y2, other.z1, other.y2)

    def __str__(self):
        return "({},{},{},{},{},{}:{})".format(self.x1, self.x2, self.y1, self.y2, self.z1, self.z2, self.volume())

    def __repr__(self):
        return self.__str__()


with open(FILE) as f:
    steps = []
    for line in f.readlines():
        lp = re.split("[=,.]", line.strip())
        steps.append((True if "on" == lp[0][:2] else False, int(lp[1]), int(lp[3]), int(lp[5]), int(lp[7]), int(lp[9]), int(lp[11])))

    reactor = []  # list of cubes which are whole lit
    counter = 0
    s = 0
    for step in steps:
        action, x1, x2, y1, y2, z1, z2 = step

        cube = Cube(*(step[1:]))

        # Slow
        # new_cubes = [cube]
        # while new_cubes:
        #     cube = new_cubes.pop()
        #
        #     # try all lit cubes in reactor
        #     new_reactor = []
        #     for c in reactor:
        #         intersection = c.intersect(cube)
        #         if intersection is not None:
        #             if action:
        #                 # turn on
        #                 new_reactor.append(c)  # keep existing cube
        #
        #                 # add new cubes for insertion
        #                 diff = cube.difference(c)
        #                 new_cubes += diff
        #                 break
        #             else:
        #                 # turn off
        #                 new_reactor += c.difference(cube)
        #         else:
        #             new_reactor.append(c)
        #     else:
        #         if action:
        #             new_reactor.append(cube)
        #         reactor = new_reactor

        # Fast: subtract current cuboid from others in reactor
        new_reactor = []

        for other in reactor:
            intersection = other.intersect(cube)
            if intersection is not None:
                for subcube in other.difference(cube):
                    new_reactor.append(subcube)
            else:
                new_reactor.append(other)

        if action:
            new_reactor.append(cube)

        reactor = new_reactor

    counter = 0
    for c in reactor:
        counter += c.volume()
    print(counter)

# Similar idea but concise and faster
# Source: https://github.com/juanplopes/advent-of-code-2021/blob/main/day22b.py


class Cuboid:
    def __init__(self, x1: int, x2: int, y1: int, y2: int, z1: int, z2: int) -> None:
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2

    def volume(self):
        return (self.x2 - self.x1) * (self.y2 - self.y1) * (self.z2 - self.z1)

    def intersect(self, other: 'Cuboid') -> Union['Cuboid', None]:
        x1 = max(self.x1, other.x1)
        x2 = min(self.x2, other.x2)

        y1 = max(self.y1, other.y1)
        y2 = min(self.y2, other.y2)

        z1 = max(self.z1, other.z1)
        z2 = min(self.z2, other.z2)

        # there is overlap between intervals
        if x1 <= x2 and y1 <= y2 and z1 <= z2:
            return Cuboid(x1, x2, y1, y2, z1, z2)

        # no intersection
        return None

    def subtract(self, b):
        intersection = self.intersect(b)

        if intersection is None:
            # return itself
            yield self
        else:
            a = self
            b = intersection

            yield Cuboid(a.x1, b.x1, a.y1, a.y2, a.z1, a.z2)  # left side
            yield Cuboid(b.x2, a.x2, a.y1, a.y2, a.z1, a.z2)  # right side
            yield Cuboid(b.x1, b.x2, a.y1, b.y1, a.z1, a.z2)  # bottom middle
            yield Cuboid(b.x1, b.x2, b.y2, a.y2, a.z1, a.z2)  # top middle
            yield Cuboid(b.x1, b.x2, b.y1, b.y2, a.z1, b.z1)  # front center
            yield Cuboid(b.x1, b.x2, b.y1, b.y2, b.z2, a.z2)  # back center

    def __str__(self):
        return "({},{},{},{},{},{}:{})".format(self.x1, self.x2, self.y1, self.y2, self.z1, self.z2, self.volume())

    def __repr__(self):
        return self.__str__()


with open(FILE) as f:
    T = []
    for line in f.readlines():
        lp = re.split("[=,.]", line.strip())
        cmd = lp[0][:2]
        x1, x2, y1, y2, z1, z2 = int(lp[1]), int(lp[3]), int(lp[5]), int(lp[7]), int(lp[9]), int(lp[11])

        # Uncomment this to get 1. part solution
        # if max(x1, x2, y1, y2, z1, z2) > CORE or min(x1, x2, y1, y2, z1, z2) < -CORE:
        #     continue

        # enlarge dimensions by one for simplicity (upper bound is not included in cuboid)
        cuboid = Cuboid(x1, x2 + 1, y1, y2 + 1, z1, z2 + 1)

        # subtract current cuboid from others in reactor
        T = [child for other in T
             for child in other.subtract(cuboid)
             if child.volume() > 0]
        if cmd == 'on':
            T.append(cuboid)

    print(sum(x.volume() for x in T))
