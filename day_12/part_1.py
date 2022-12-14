# Authored by Carlos Serra-Toro (https://carlosserratoro.com)
# See the file LICENSE for the licence
import array
import os
import sys


def build_territory(input_file):
    """Build the territory, return it along with start and end positions"""
    territory = []
    start_pos = None
    end_pos = None
    with open(input_file) as f:
        for line_no, line in enumerate(f):
            territory.append(array.array('B', []))
            for letter_no, letter in enumerate(line.rstrip(os.linesep)):
                if letter == 'S':
                    start_pos = (line_no, letter_no)
                elif letter == 'E':
                    end_pos = (line_no, letter_no)
                territory[-1].append(ord(letter))
    return territory, start_pos, end_pos


def feasible_neighbours(territory, pos):
    neighbours = []
    num_rows = len(territory)
    num_cols = len(territory[0])
    for row_offset in (-1, +1):
        for col_offset in (-1, +1):
            if 0 <= row_offset < num_rows and 0 <= col_offset < num_cols:
                neighbours.append((pos + row_offset, pos + col_offset))
    return neighbours


def part_1(territory, start, destination):
    return _part_1(
        territory=territory,
        destination=destination,
        current=start,
        previous=None,
        visited=set(),
        h=dict())


def _part_1(territory, destination, current, previous, visited, h):
    if current == destination:
        return 1

    if (previous, current) in h:
        return h[previous, current]

    min_steps = sys.maxsize
    min_steps_neighbour = None
    for next_cell in feasible_neighbours(territory, current):
        steps = _part_1(territory, destination, next_cell, current, visited, h)
        visited.add(steps)
        if steps < min_steps:
            min_steps = steps
            min_steps_neighbour = next_cell
    h[current, min_steps_neighbour] += min_steps

    return h[current, min_steps_neighbour]


if __name__ == '__main__':
    print(build_territory('inputs/part_1_test.txt'))
