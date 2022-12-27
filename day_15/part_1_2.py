# Authored by Carlos Serra-Toro (https://carlosserratoro.com)
# See the file LICENSE for the licence
import re
import math
from dataclasses import dataclass


DISTRESS_SIGNAL_X_MULT_MAGIC_NUM = 4000000


@dataclass(frozen=True)
class Point:
    """A 2-dimensional point."""
    x: int
    y: int


class CircleManhattan:
    """A circle using the Manhattan distance."""

    def __init__(self, circle_id, center, point):
        """Build a circle from its center and one point in its perimeter."""
        self.id = circle_id
        self.center = center
        self.radius = self._manhattan(center, point)

    def get_x(self, y):
        """Given Y coordinate, return the two Xs of its circumference.

        For a circle having the center at (a,b) and radius r, a point (x,y)
        satisfies |x-a| + |y-b| == r, thus x = {r - |y-b| + a, -r + |y-b| + a}.
        """
        x_left = -self.radius + abs(y - self.center.y) + self.center.x
        x_right = self.radius - abs(y - self.center.y) + self.center.x
        return x_left, x_right

    @classmethod
    def _manhattan(cls, point_1, point_2):
        """Manhattan distance for 2-dimensional points."""
        return abs(point_1.x - point_2.x) + abs(point_1.y - point_2.y)


def load_circles_beacons(input_file):
    """Load the circles and beacons from the input file."""
    circles = []
    beacons = set()
    with open(input_file) as f:
        for line_no, line in enumerate(f, start=1):
            sensor_x, sensor_y, beacon_x, beacon_y = map(
                int, re.findall(r'-?\d+', line))
            beacon_point = Point(beacon_x, beacon_y)
            circles.append(
                CircleManhattan(
                    circle_id=line_no,
                    center=Point(sensor_x, sensor_y),
                    point=beacon_point)
            )
            beacons.add(beacon_point)
    return circles, beacons


def get_bounding_box(circles):
    """Get the bounding box made by all the circles."""
    inf = math.inf
    min_x, min_y, max_x, max_y = inf, inf, -inf, -inf
    for circle in circles:
        center = circle.center
        r = circle.radius
        min_x = min(min_x, center.x - r)
        max_x = max(max_x, center.x + r)
        min_y = min(min_y, center.y - r)
        max_y = max(max_y, center.y + r)
    return min_x, min_y, max_x, max_y


def ranges_intersect(r_1, r_2):
    """Whether two ranges intersect.

    The ranges are for integers, so consecutive integers
    are meant to intersect. For example, (1, 2) and (3, 4)
    intersect because 2 and 3 are consecutive in the space
    of integers.

    >>> ranges_intersect((1, 3), (3, 6))
    True
    >>> ranges_intersect((1, 3), (2, 4))
    True
    >>> ranges_intersect((1, 3), (5, 7))
    False
    >>> ranges_intersect((1, 2), (3, 4))
    True
    >>> ranges_intersect((3, 4), (1, 2))
    True
    """
    return (
        r_1[0] <= r_2[1] and r_2[0] <= r_1[1]
        or abs(r_1[1] - r_2[0]) == 1
        or abs(r_2[1] - r_1[0]) == 1
    )


def ranges_merge(r_1, r_2):
    """Merge two ranges into one.

    >>> ranges_merge((1, 3), (2, 4))
    (1, 4)
    """
    assert ranges_intersect(r_1, r_2), 'Ranges do not intersect.'
    return min(r_1[0], r_2[0]), max(r_1[1], r_2[1])


def ranges_flatten(ranges):
    """Flatten several ranges into non-overlapping ones.

    >>> ranges_flatten([(1, 3), (2, 5), (7, 9), (9, 10)])
    [(1, 5), (7, 10)]
    >>> ranges_flatten([(1, 2), (3, 4), (5, 6), (7, 8)])
    [(1, 8)]
    >>> ranges_flatten([(1, 2), (4, 5), (7, 8)])
    [(1, 2), (4, 5), (7, 8)]
    """
    ranges.sort()
    flat_ranges = [ranges[0]] if ranges else []
    for r in ranges:
        if ranges_intersect(flat_ranges[-1], r):
            flat_ranges.append(ranges_merge(flat_ranges.pop(), r))
        else:
            flat_ranges.append(r)
    return flat_ranges


def ranges_not_covered(flat_ranges, start, end):
    """Return ranges not covered by `flattened_ranges` between (start, end).

    >>> ranges_not_covered([(0, 10)], start=0, end=10)
    []
    >>> ranges_not_covered([(2, 8)], start=0, end=10)
    [(0, 1), (9, 10)]
    >>> ranges_not_covered([(1, 5), (7, 9)], start=0, end=10)
    [(0, 0), (6, 6), (10, 10)]
    >>> ranges_not_covered([(1, 1)], start=0, end=10)
    [(0, 0), (2, 10)]
    """
    ranges = []
    assert start <= flat_ranges[0][0], 'Wrong start.'
    assert end >= flat_ranges[-1][1], 'Wrong end.'
    for i in range(len(flat_ranges)):
        if i == 0 and abs(flat_ranges[0][0] - start) >= 1:
            ranges.append((start, flat_ranges[0][0] - 1))
        if i > 0:
            ranges.append((flat_ranges[i-1][1] + 1, flat_ranges[i][0] - 1))
        if i == len(flat_ranges) - 1 and abs(flat_ranges[-1][1] - end) >= 1:
            ranges.append((flat_ranges[-1][1] + 1, end))
    return ranges


def get_num_beacons_in_range(beacons, r, y):
    """Get the number of beacons in a range `r` at a given Y."""
    num_beacons = 0
    for beacon in beacons:
        if beacon.y == y and r[0] <= beacon.x <= r[1]:
            num_beacons += 1
    return num_beacons


def get_num_x_coordinates_without_beacon(y, circles, beacons):
    """Get number of X coordinates not covered by any circle for a given Y."""

    # Get the ranges of x-coordinates covered by any circle.
    ranges_cover = []
    for c in circles:
        if c.center.y - c.radius <= y <= c.center.y + c.radius:
            ranges_cover.append(c.get_x(y))
    ranges_flat = ranges_flatten(ranges_cover)

    # Get those X covered by a circle and that are not beacons.
    num_x = 0
    for r in ranges_flat:
        num_beacons = get_num_beacons_in_range(beacons, r, y=y)
        num_x += r[1] - r[0] + 1 - num_beacons
    return num_x


def limit_range(r, min_val, max_val):
    """Limit the extremes of a range.

    >>> limit_range((1, 3), min_val=0, max_val=4)
    (1, 3)
    >>> limit_range((1, 3), min_val=1, max_val=3)
    (1, 3)
    >>> limit_range((1, 3), min_val=2, max_val=2)
    (2, 2)
    >>> limit_range((2, 2), min_val=2, max_val=2)
    (2, 2)
    >>> limit_range((1, 3), min_val=4, max_val=5)
    ()
    """
    assert r[0] <= r[1], 'Range (a, b) must satisfy a <= b'
    left_r = r[0] if r[0] >= min_val else min_val
    right_r = r[1] if r[1] <= max_val else max_val
    return (left_r, right_r) if left_r <= right_r else ()


def get_tuning_frequency(circles, x_domain, y_domain):
    """Tuning frequency comes from the only point not covered by sensors"""
    for y in range(y_domain[0], y_domain[1]+1):

        # Get the ranges of x-coordinates covered by any circle.
        ranges_cover = []
        for c in circles:
            if c.center.y - c.radius <= y <= c.center.y + c.radius:
                ranges_cover.append(
                    limit_range(
                        c.get_x(y),
                        min_val=x_domain[0],
                        max_val=x_domain[1])
                )
        ranges_flat = ranges_flatten(ranges_cover)

        # Get those X coordinates not covered by any circle, if any.
        ranges_no_cover = ranges_flatten(
            ranges_not_covered(
                ranges_flat,
                start=x_domain[0],
                end=x_domain[1])
        )
        if ranges_no_cover:
            return ranges_no_cover[0][0] * DISTRESS_SIGNAL_X_MULT_MAGIC_NUM + y
    return -1


def part_1():
    """Part 1 of Day 15"""
    circles_test, beacons_test = load_circles_beacons(
        'inputs/part_1_2_test.txt')
    assert 26 == get_num_x_coordinates_without_beacon(
        y=10, circles=circles_test, beacons=beacons_test)

    circles, beacons = load_circles_beacons(
        'inputs/part_1_2.txt')
    assert 4873353 == get_num_x_coordinates_without_beacon(
        y=2000000, circles=circles, beacons=beacons)


def part_2():
    """Part 2 of Day 15"""
    circles_test, _ = load_circles_beacons(
        'inputs/part_1_2_test.txt')
    assert 56000011 == get_tuning_frequency(
        circles=circles_test, x_domain=(0, 20), y_domain=(0, 20))

    circles, _ = load_circles_beacons(
        'inputs/part_1_2.txt')
    max_x = 4000000
    max_y = 4000000
    assert 11600823139120 == get_tuning_frequency(
        circles=circles, x_domain=(0, max_x), y_domain=(0, max_y))


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    part_1()
    part_2()
