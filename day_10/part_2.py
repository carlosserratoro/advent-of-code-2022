# Authored by Carlos Serra-Toro (https://carlosserratoro.com)
# See the file LICENSE for the licence
import os
import re


CRT_WIDTH = 40
CRT_HEIGHT = 6


def get_instruction_lines(source_file):
    with open(source_file) as f:
        for line in f:
            yield line.rstrip(os.linesep)


def hit_on_crt(crt, num_cycle, x):
    """Whether we had a hit in the CRT"""
    num_pixel = num_cycle - 1
    row, col = divmod(num_pixel, CRT_WIDTH)
    if x-1 <= col <= x+1:
        crt.add((row, col))


def compute_crt(instructions):
    """Compute the pixels on the CRT that will be displayed"""
    crt = set()
    x = 1
    num_cycle = 1
    for instruction in instructions:
        if instruction == 'noop':
            hit_on_crt(crt, num_cycle, x)
            num_cycle += 1
        else:  # instruction is `addx <value>`
            add_to_x = int(re.search(r'-?\d+$', instruction)[0])
            hit_on_crt(crt, num_cycle, x)
            num_cycle += 1
            hit_on_crt(crt, num_cycle, x)
            num_cycle += 1
            x += add_to_x
    return crt


def draw_crt(crt):
    """Draw the CRT according to the pixels to highlight"""
    for row in range(CRT_HEIGHT):
        for col in range(CRT_WIDTH):
            print('#' if (row, col) in crt else '.', end='')
        print()


if __name__ == '__main__':
    draw_crt(compute_crt(get_instruction_lines('inputs/part_1_2.txt')))
