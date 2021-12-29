# https://adventofcode.com/2021/day/19

import math
import re
from math import sin, cos
import numpy as np

from collections import Counter, defaultdict

FILE = 'input.txt'
# FILE = 'input-small.txt'

D = 3
OVERLAP = 12

THETA = np.pi / 2
RANGE = 1000


def r_x(theta: int) -> np.array:
    return np.array([
        [1, 0, 0],
        [0, cos(theta), -sin(theta)],
        [0, sin(theta), cos(theta)],
    ], dtype=int)


def r_y(theta: int) -> np.array:
    return np.array([
        [cos(theta), 0, sin(theta)],
        [0, 1, 0],
        [-sin(theta), 0, cos(theta)],
    ], dtype=int)


def r_z(theta: int) -> np.array:
    return np.array([
        [cos(theta), -sin(theta), 0],
        [sin(theta), cos(theta), 0],
        [0, 0, 1],
    ], dtype=int)


with open(FILE) as f:
    sensors = []
    beacons = []

    for line in f.readlines():
        if line[0:3] == '---':
            continue

        if len(line.strip()) == 0:
            sensors.append(beacons)
            beacons = []
            continue

        beacons.append(np.array([list(map(int, line.strip().split(',')))], dtype=int))
    sensors.append(beacons)

    # print(sensors)

    # Generate all possible scanner orientations
    # In total, each scanner could be in any of 24 different orientations:
    # facing positive or negative x, y, or z, and considering any of four directions "up" from that facing.
    rotations = []
    for tz in [0, math.pi]:
        for tx in [0, math.pi / 2, math.pi, math.pi * 3 / 2]:
            rotations.append(r_z(tz).dot(r_x(tx)))
    for tz in [np.pi / 2, np.pi * 3 / 2]:
        for ty in [0, math.pi / 2, math.pi, math.pi * 3 / 2]:
            rotations.append(r_z(tz).dot(r_y(ty)))
    for ty in [np.pi / 2, np.pi * 3 / 2]:
        for tz in [0, math.pi / 2, math.pi, math.pi * 3 / 2]:
            rotations.append(r_y(ty).dot(r_z(tz)))

    # as if scanner 0 is at (0,0,0)
    beacons = set([tuple(b[0]) for b in sensors[0]])
    sensor_position = {0: np.array([[0, 0, 0]])}
    sensor_rotation = {0: np.eye(3, dtype=int)}

    # precompute all rotations for all sensors
    rotated_sensors = defaultdict(dict)
    for i, s in enumerate(sensors):
        for j, r in enumerate(rotations):
            rotated_sensors[i][j] = [r.dot(b.T) for b in s]

    sensor_pairs = []

    processed_sensors = set()
    sensors2process = {0}

    # for each unprocessed sensor
    while len(processed_sensors) != len(sensors):
        i = sensors2process.pop()
        s1 = sensors[i]
        processed_sensors.add(i)

        s1_set = set()
        for b1 in s1:
            s1_set.add(tuple(b1[0]))

        # try other unprocessed sensors
        for j in range(len(sensors)):
            if j in processed_sensors or j in sensors2process:
                continue

            s2 = sensors[j]

            # try matching in every rotation
            print("searching ", i, j)
            for ir, r in enumerate(rotations):
                # s3 = [r.dot(b.T) for b in s2]
                s3 = rotated_sensors[j][ir]

                # try mapping b2 to every b1
                matched_translation = None
                for ib2tc, b2_translation_candidate in enumerate(s3):
                    for ib1tc, b1_translation_candidate in enumerate(s1):
                        translation = np.subtract(b2_translation_candidate.T, b1_translation_candidate)
                        # print("transl ", translation, b2_translation_candidate.T, b1_translation_candidate)

                        pos1 = sensor_position[i]
                        rot1 = sensor_rotation[i]

                        pos2 = np.subtract(pos1, rot1.dot(translation.T).T)
                        rot2 = rot1.dot(r)

                        diff = np.abs(np.subtract(pos1, pos2))
                        if diff[0][0] > 2*RANGE or diff[0][1] > 2*RANGE or diff[0][2] > 2*RANGE:
                        # if diff[0][0] > RANGE and diff[0][1] > RANGE and diff[0][2] > RANGE:
                            # print("out of range", pos1, pos2, diff)
                            continue

                        # sensor_position[j] = pos2


                        s3_set = set()
                        for b2 in s3:
                            # b2t = np.eye(3, dtype=int)
                            b2t = np.subtract(b2.T, translation)
                            # print(tuple(b2t[0]))
                            s3_set.add(tuple(b2t[0]))

                        intersection = s1_set.intersection(s3_set)
                        if len(intersection) >= OVERLAP:
                            print("match found, overlap ", len(intersection))
                            sensors2process.add(j)
                            matched_translation = translation
                            sensor_pairs.append((i, j, r, translation))

                            sensor_position[j] = pos2
                            sensor_rotation[j] = rot2
                            break

                        if len(s1) - ib1tc < OVERLAP:
                            # print("2 shortcut", len(s1), ib1tc, len(s1) - ib1tc, OVERLAP)
                            break

                    if matched_translation is not None:
                        break

                    if len(s3) - ib2tc < OVERLAP:
                        # print("shortcut", len(s3), ib2tc, len(s3) - ib2tc, OVERLAP)
                        break

                if matched_translation is not None:
                    break

    print(sensor_pairs)

    for i, j, r, t in sensor_pairs:
        pos1 = sensor_position[i]
        rot1 = sensor_rotation[i]

        pos2 = np.subtract(pos1, rot1.dot(t.T).T)
        sensor_position[j] = pos2

        rot2 = rot1.dot(r)
        sensor_rotation[j] = rot2

        for b in sensors[j]:
            bt = np.add(pos2, rot2.dot(b.T).T)
            beacons.add(tuple(bt[0]))

    # for b in beacons:
    #     print("{},{},{}".format(b[0], b[1], b[2]))

    print(sensor_position)
    print(len(beacons))  # 1. part

    max_manhattan_distance = 0


    def manhattan_distance(sp1, sp2):
        return np.sum(np.abs(np.subtract(sp1, sp2)))


    for i in range(len(sensor_position)):
        for j in range(i + 1, len(sensor_position)):
            max_manhattan_distance = max(max_manhattan_distance, manhattan_distance(sensor_position[i], sensor_position[j]))

    print(max_manhattan_distance)  # 2. part
