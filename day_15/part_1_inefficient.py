# Authored by Carlos Serra-Toro (https://carlosserratoro.com)
# See the file LICENSE for the licence

# NOTE: This was my first attempt to solve this Day 15. But I used here
#       a naive approach that made it run slow (but acceptable to solve
#       the Part 1) and totally unusable to solve the Part 2.

import re
import math


def manhattan_2d(pos_1, pos_2):
    """Manhattan distance for 2-dimensional points"""
    return abs(pos_1[0] - pos_2[0]) + abs(pos_1[1] - pos_2[1])


class NearestNeighbour:

    def __init__(self, input_file, metric=manhattan_2d):
        # The nearest neighbour map, with h: sensor -> beacon
        self._nn = dict()

        # The bounding box of the 2D space: (min_x, min_y, max_x, max_y)
        self._bb = None

        # The metric to use to compute the distances between the points.
        self._metric = metric

        self._load_nn_from_file(input_file)

    def get_bounding_box(self):
        """Get the bounding box, (min_x, min_y, max_x, max_y)

        The bounding box is determined by the range of each sensor.
        """
        if not self._bb:
            inf = math.inf
            min_x, min_y, max_x, max_y = inf, inf, -inf, -inf
            for sensor in self.get_sensors():
                radius = self._metric(sensor, self.get_closest_beacon(sensor))
                min_x = min(min_x, sensor[0] - radius)
                max_x = max(max_x, sensor[0] + radius)
                min_y = min(min_y, sensor[1] - radius)
                max_y = max(max_y, sensor[1] + radius)
            self._bb = (min_x, min_y, max_x, max_y)
        return self._bb

    def get_closest_beacon(self, pos):
        return self._nn.get(pos, None)

    def get_sensors(self):
        """Get the list of sensors"""
        return tuple(self._nn.keys())

    def is_beacon(self, pos):
        """Is there a beacon at the coordinate?"""
        return pos in self._nn.values()

    def is_sensor(self, pos):
        """Is there a sensor at the coordinate?"""
        return pos in self._nn.keys()

    def _load_nn_from_file(self, input_file):
        with open(input_file) as f:
            for line in f:
                sensor_x, sensor_y, beacon_x, beacon_y = map(
                    int, re.findall(r'-?\d+', line))
                self._nn[sensor_x, sensor_y] = beacon_x, beacon_y


def get_beacon_free_positions_at_row(nn, y):
    positions_without_beacon = []

    bb = nn.get_bounding_box()
    min_x, max_x = bb[0], bb[2]

    # Precompute the distance of each sensor to its closest beacon
    dist_sensor_to_closest_beacon = dict()
    for sensor in nn.get_sensors():
        dist_sensor_to_closest_beacon[sensor] = manhattan_2d(
            sensor, nn.get_closest_beacon(sensor))

    # We know, for each sensor, which is its closest beacon. So, for a given
    # position, we see if that position is outside the range of the sensor.
    # If a position is out of the ranges of all the sensors, then we may have
    # a beacon there. In reverse, if a position is within the range of at least
    # one sensor, and that position itself is not already a beacon, then we can
    # discard that position being a potential beacon.
    for x in range(min_x, max_x + 1):
        pos = (x, y)
        if not nn.is_beacon(pos) and not nn.is_sensor(pos):
            cannot_contain_beacon = False
            for sensor in nn.get_sensors():
                dist_to_sensor = manhattan_2d(pos, sensor)
                if dist_to_sensor <= dist_sensor_to_closest_beacon[sensor]:
                    cannot_contain_beacon = True
                    break
            if cannot_contain_beacon:
                positions_without_beacon.append(pos)
    return positions_without_beacon


def part_1():
    nn_test = NearestNeighbour('inputs/part_1_test.txt')
    assert 26 == len(get_beacon_free_positions_at_row(nn_test, y=10))

    nn = NearestNeighbour('inputs/part_1.txt')
    assert 4873353 == len(get_beacon_free_positions_at_row(nn, y=2000000))


if __name__ == '__main__':
    part_1()
