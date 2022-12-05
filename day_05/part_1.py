# Authored by Carlos Serra-Toro (https://carlosserratoro.com)
# See the file LICENSE for the licence
import os
import re
from collections import deque


def get_lines(source_file):
    with open(source_file) as f:
        for line in f:
            yield line


def create_stack_layout(stacks, line):
    """Create the stack layout by updating parameter `stacks`

    Here we take advantage of the fact that the input for
    the layout is tabulated and follows the pattern of:
    '[', single letter, ']', white space, so a length of 4.
    We use this known format to scan the input in an efficient
    way.
    """

    chars_per_stack = 4  # Four chars per stack.

    # Since we build the stacks online, if we find
    # new stacks we have to dinamically extend the list
    # of stacks we are using. In the test file we are
    # given lines that are always of the same size, no
    # matter if they contain data for just one stack, so
    # we could make an allocation outside this method.
    num_stacks = len(line) // chars_per_stack
    if num_stacks > len(stacks):
        num_new_stacks = num_stacks - len(stacks)
        stacks.extend(deque() for _ in range(num_new_stacks))

    for num_stack in range(num_stacks):
        letter_pos = num_stack * chars_per_stack + 1
        letter = line[letter_pos]

        if letter != ' ':
            # We are given the stack from top to bottom, that's
            # why we are using a deque to efficiently build the
            # stack and don't have to reverse it later.
            stacks[num_stack].appendleft(letter)


def modify_stack_layout(stacks, line):
    """Modify the `stack` layouts by applying operation in `line`"""
    num_ops, from_stack, to_stack = map(int, re.findall(r'\d+', line))
    for _ in range(num_ops):
        item = stacks[from_stack - 1].pop()
        stacks[to_stack - 1].append(item)


def get_tops(lines):
    """Return the top of all the stacks"""

    # We have a list of stacks. Each stack is represented
    # using a deque because at first we are given the layout
    # from top to bottom. We could invert the queue but the
    # deque allows us to add/remove in O(1) from both sides.
    stacks = []

    # Here it is key to make this efficient, taking advantage
    # of what we know: we will be given first the layout, then
    # the operations over that layout, and we'll never get an
    # error because of not popping out elements from an empty
    # stack and so on. We process the lines one by one, assuming
    # an input of an arbitrary length.
    for line in lines:

        # Operation lines are the most common, and they come
        # always after the lines that define the layout, and
        # the always start with the word 'move'. Being the
        # most common ones, we process them first to save jumps.
        if line and line[0] == 'm':
            modify_stack_layout(stacks, line)

        # Lines defining the layout are non-empty lines that
        # contain a '['. We can determine faster than this if
        # a line is one of a layout, because we know the other
        # two kind of lines (that we don't care about) are
        # either the separator line (which is an empty line) or
        # the line numbering the stacks (that contain a list of
        # consecutive numbers starting in ' 1'). So if we are not
        # any of those two other types, then we are on a line that
        # defines the layout.
        elif line != os.linesep and line[1] != '1':
            create_stack_layout(stacks, line)

    # Print the tops
    tops = []
    for stack in stacks:
        tops.append(stack[-1])
    return ''.join(tops)


if __name__ == '__main__':
    print(get_tops(get_lines('inputs/part_1_2.txt')))
