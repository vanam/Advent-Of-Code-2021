# https://adventofcode.com/2021/day/19

import math
from collections import defaultdict
from math import sin, cos

import numpy as np

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
    sensor_positions = {0: np.array([[0, 0, 0]])}
    sensor_rotations = {0: np.eye(3, dtype=int)}

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

        # try other unprocessed sensors
        for j in range(len(sensors)):
            if j in processed_sensors or j in sensors2process:
                continue

            # try matching in every rotation
            # print("Searching", i, j)
            for ir, r in enumerate(rotations):
                s3 = rotated_sensors[j][ir]

                # vote for sensor position
                sensor_position_vote = defaultdict(int)

                # try mapping b2 to every b1
                matched_translation = None
                for b2_translation_candidate in s3:
                    for b1_translation_candidate in s1:
                        translation = np.subtract(b2_translation_candidate.T, b1_translation_candidate)
                        sensor_position_vote[tuple(translation[0])] += 1

                for translation, cnt in sensor_position_vote.items():
                    if cnt >= OVERLAP:
                        # print("Match found, overlap size:", cnt)
                        translation = np.array(translation)

                        pos1 = sensor_positions[i]
                        rot1 = sensor_rotations[i]

                        pos2 = np.subtract(pos1, rot1.dot(translation.T).T)
                        rot2 = rot1.dot(r)

                        sensors2process.add(j)
                        matched_translation = translation
                        sensor_pairs.append((i, j, r, translation))

                        sensor_positions[j] = pos2
                        sensor_rotations[j] = rot2

                if matched_translation is not None:
                    break

    # Reconstruct final beacon positions
    # print(sensor_pairs)
    for i, j, r, t in sensor_pairs:
        pos2 = sensor_positions[j]
        rot2 = sensor_rotations[j]

        for b in sensors[j]:
            bt = np.add(pos2, rot2.dot(b.T).T)
            beacons.add(tuple(bt[0]))

    # Print beacons
    # for b in beacons:
    #     print("{},{},{}".format(b[0], b[1], b[2]))

    # Print sensor positions
    # print(sensor_position)
    print(len(beacons))  # 1. part

    def manhattan_distance(sp1, sp2):
        return np.sum(np.abs(np.subtract(sp1, sp2)))

    max_manhattan_distance = 0
    for i in range(len(sensor_positions)):
        for j in range(i + 1, len(sensor_positions)):
            max_manhattan_distance = max(max_manhattan_distance, manhattan_distance(sensor_positions[i], sensor_positions[j]))

    print(max_manhattan_distance)  # 2. part
