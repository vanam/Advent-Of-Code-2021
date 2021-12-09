# https://adventofcode.com/2021/day/5

FILE = 'input.txt'
# FILE = 'input-small.txt'


# 1. part - find line overlap

from queue import PriorityQueue
import itertools


class Segment:
    def __init__(self, x0, y0, x1, y1):
        # first point is always the left most
        # if x is equal then first point has smaller y
        if x0 < x1:
            self.x0 = x0
            self.y0 = y0
            self.x1 = x1
            self.y1 = y1
        elif x0 > x1:
            self.x0 = x1
            self.y0 = y1
            self.x1 = x0
            self.y1 = y0
        elif y0 <= y1:
            self.x0 = x0
            self.y0 = y0
            self.x1 = x1
            self.y1 = y1
        else:
            self.x0 = x1
            self.y0 = y1
            self.x1 = x0
            self.y1 = y0

    def get_y_segment_at_x(self, x):
        # assume we don't ask for this if line segment is not active at x

        # diagonal segment
        if self.x0 != self.x1 and self.y0 != self.y1:
            px = x
            delta = x - self.x0
            py = self.y0 + delta if self.y0 < self.y1 else self.y0 - delta

            return Segment(px, py, px, py)  # point
        elif self.x0 == self.x1:
            # vertical segment
            return self
        else:
            # horizontal segment
            assert(self.y0 == self.y1)
            return Segment(x, self.y0, x, self.y0)  # point

    def intersect(self, other, x) -> list:
        # rough check if there might be an overlap
        # y0 = max(self.y0, other.y0)
        # y1 = min(self.y1, other.y1)
        #
        # if y0 > y1:
        #     return []
        # problem with diagonal lines upward

        # proper check
        s1 = self.get_y_segment_at_x(x)
        s2 = other.get_y_segment_at_x(x)

        y0 = max(s1.y0, s2.y0)
        y1 = min(s1.y1, s2.y1)

        if y0 <= y1:
            y_overlap = [x for x in range(y0, y1 + 1)]
            # print(self, ' vs ', other, " overlaps at ", x, y_overlap)
            return y_overlap
        return []

        # # assume only horizontal or vertical lines
        # # x axis is covered by line sweep
        # # check y axis overlap
        #
        #
        # y0 = max(self.y0, other.y0)
        # y1 = min(self.y1, other.y1)
        #
        # # there is overlap between intervals
        # if y0 <= y1:
        #     y_overlap = [x for x in range(y0, y1 + 1)]
        #     # print(self, ' vs ', other, " overlaps at ", x, y_overlap)
        #     return y_overlap
        # return []

    def __eq__(self, other):
        return self.x0 == other.x0 and self.y0 == other.y0 and self.x1 == other.x1 and self.y1 == other.y1

    def __lt__(self, other):
        if self.x0 == other.x0:
            if self.y0 == other.y0:
                if self.x1 == other.x1:
                    return self.y1 < other.y
                else:
                    return self.x1 < other.x1
            else:
                return self.y0 < other.y0
        else:
            return self.x0 < other.x0

    def __hash__(self):
        return hash((self.x0, self.y0, self.x1, self.y1))

    def __str__(self):
        return "%d, %d -> %d %d" % (self.x0, self.y0, self.x1, self.y1)


with open(FILE) as f:
    lines = f.readlines()
    segments = PriorityQueue()

    for line in lines:
        line = line.strip()
        args = list(itertools.chain(*[list(map(int, p.split(','))) for p in line.split(' -> ')]))

        # keep only horizontal or vertical segments
        if args[0] != args[2] and args[1] != args[3]:
            pass
            # print("skippint ", *args)
            # continue  # Uncomment this to get part 1 result

        segments.put(Segment(*args))

    counter = 0
    active_segments = set()
    x = 0  # start at x and move it until we have no more line segments
    while len(active_segments) > 0 or not segments.empty():
        # find if elements in PQ starts at x
        while not segments.empty():
            segment = segments.get()
            if segment.x0 == x:
                # print("adding ", segment, " at ", x)
                active_segments.add(segment)
            else:
                # print("segment ", segment, " doesnt start at ", x)
                segments.put(segment)  # put it back
                break  # There will be no other line segments in priority queue

        y_intersections = set()  # set of intersections at x

        # try intersections between all pairs of line segments
        active_segments_list = list(active_segments)
        for i in range(len(active_segments_list)):
            for j in range(i + 1, len(active_segments_list)):
                s1 = active_segments_list[i]
                s2 = active_segments_list[j]

                ys = s1.intersect(s2, x)
                y_intersections.update(ys)

        # TODO line sweep in y axis

        # remove all line segments which ends at x
        for s in active_segments_list:
            if s.x1 == x:
                active_segments.remove(s)
                # print("Removing ", s)

        # add number of intersections
        counter += len(y_intersections)

        # move one to the right with line sweep
        x += 1

    print(counter)
# 2. part
