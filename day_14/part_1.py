# Authored by Carlos Serra-Toro (https://carlosserratoro.com)
# See the file LICENSE for the licence
import sys
from collections import namedtuple


# A segment is a pair of coordinates (x, y)
Segment = namedtuple('Segment', ['start', 'end'])


def load_rocks_segments(rocks_file):
    """Load the rocks and return a list of segments"""
    return []


def get_start_of_abyss(rocks):
    """Return the Y position in which the abyss starts"""
    abyss = -1
    for segment in rocks:
        start, end = segment
        if start[1] > abyss:
            abyss = start[1]
        if end[1] > abyss:
            abyss = end[1]
    return abyss + 1


def grain_falls_forever(grain, start_of_abyss):
    return grain[1] >= start_of_abyss


def occupied(pos, offset, sand, rocks_segments):
    """Whether the pos + offset is occupied"""
    new_pos = (pos[0] + offset[0], pos[1] + offset[1])
    if new_pos in sand:
        return True
    if


def grain_is_in_rest(grain, sand, rocks_segments):
    """Grain is in rest if below, below-left or below-right is occupied"""
    return (
        occupied(grain, (0, +1), sand, rocks_segments)
        or occupied(grain, (+1, +1), sand, rocks_segments)
        or occupied(grain, (-1, +1), sand, rocks_segments)
    )


def move_grain(grain, sand, rocks_segments):
    pass


def part_1(input_file):
    rocks_segments = load_rocks_segments(input_file)
    start_of_abyss = get_start_of_abyss(rocks_segments)
    sand = set()

    grain = (500, 0)
    while not grain_falls_forever(grain, start_of_abyss):
        in_rest = grain_is_in_rest(grain, sand, rocks_segments)
        if in_rest:
            sand.add(grain)  # Add the grain to the pile of sand.
            grain = (500, 0)  # Generate a new grain
        else:
            grain = move_grain(grain, sand, rocks_segments)


if __name__ == '__main__':
    part_1('inputs/part_1.txt')
