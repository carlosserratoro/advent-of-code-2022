# Authored by Carlos Serra-Toro (https://carlosserratoro.com)
# See the file LICENSE for the licence
import os


def get_instructions(source_file):
    with open(source_file) as f:
        for line in f:
            instruction = line.rstrip(os.linesep).split(' ')
            direction, steps = instruction[0], int(instruction[1])
            yield direction, steps


def move_head(head, direction):
    """Move the head one step into the direction"""
    if direction == 'L':
        return head[0], head[1] - 1
    if direction == 'R':
        return head[0], head[1] + 1
    if direction == 'U':
        return head[0] + 1, head[1]
    if direction == 'D':
        return head[0] - 1, head[1]


def drag_tail(head, direction):
    """Drag the tail to follow the head, both being not adjacent"""
    if direction == 'L':
        return head[0], head[1] + 1
    if direction == 'R':
        return head[0], head[1] - 1
    if direction == 'U':
        return head[0] - 1, head[1]
    if direction == 'D':
        return head[0] + 1, head[1]


def are_distant(head, tail):
    return (
        abs(head[0] - tail[0]) >= 2
        or abs(head[1] - tail[1]) >= 2
    )


def get_num_positions_visited(instructions):
    head = (0, 0)
    tail = (0, 0)
    positions = {tail}
    for direction, steps in instructions:
        for _ in range(steps):
            head = move_head(head, direction)
            if are_distant(head, tail):
                tail = drag_tail(head, direction)
                positions.add(tail)
    return len(positions)


if __name__ == '__main__':
    print(get_num_positions_visited(
        get_instructions('inputs/part_1_2.txt')))
