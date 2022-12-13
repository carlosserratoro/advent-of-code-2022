# Authored by Carlos Serra-Toro (https://carlosserratoro.com)
# See the file LICENSE for the licence
import os


NUM_KNOTS = 10


class Rope:
    def __init__(self):
        self._knots = [(0, 0) for _ in range(NUM_KNOTS)]

    def get_tail_position(self):
        return self._knots[NUM_KNOTS-1]

    def _are_adjacent(self, knot_a, knot_b):
        return (
            abs(knot_a[0] - knot_b[0]) <= 1
            and abs(knot_a[1] - knot_b[1]) <= 1
        )

    def _compute_vector_from_direction(self, knot, direction):
        knot_pos = self._knots[knot]
        if direction == 'L':
            return knot_pos[0], knot_pos[1] - 1
        if direction == 'R':
            return knot_pos[0], knot_pos[1] + 1
        if direction == 'U':
            return knot_pos[0] + 1, knot_pos[1]
        if direction == 'D':
            return knot_pos[0] - 1, knot_pos[1]

    def _compute_vector_from_knots(self, knot_current, knot_next):
        current_knot_pos = self._knots[knot_current]
        next_knot_pos = self._knots[knot_next]
        return (
            next_knot_pos[0] - current_knot_pos[0],
            next_knot_pos[1] - current_knot_pos[1],
        )

    def _compute_new_pos(self, knot, vector):
        knot_pos = self._knots[knot]
        return (
            knot_pos[0] + vector[0],
            knot_pos[1] + vector[1],
        )

    def stretch(self, direction):
        for i in range(NUM_KNOTS - 1):
            if self._are_adjacent(self._knots[i], self._knots[i+1]):
                vector = self._compute_vector_from_direction(i, direction)
            else:
                vector = self._compute_vector_from_knots(i, i+1)
            current_knot_pos = self._compute_new_pos(i, vector)
            self._knots[i] = current_knot_pos
            if self._are_adjacent(self._knots[i], self._knots[i+1]):
                break


def get_instructions(source_file):
    with open(source_file) as f:
        for line in f:
            instruction = line.rstrip(os.linesep).split(' ')
            direction, steps = instruction[0], int(instruction[1])
            yield direction, steps


def get_num_different_positions_tail(instructions):
    tail_positions = set()
    rope = Rope()
    for direction, steps in instructions:
        for _ in range(steps):
            rope.stretch(direction)
            tail_positions.add(rope.get_tail_position())
    return len(tail_positions)


if __name__ == '__main__':
    print(get_num_different_positions_tail(
        get_instructions('inputs/part_1_2_test.txt')))
