# Authored by Carlos Serra-Toro (https://carlosserratoro.com)
# See the file LICENSE for the licence
import os
import re


def get_instruction_lines(source_file):
    with open(source_file) as f:
        for line in f:
            yield line.rstrip(os.linesep)


def compute_signal_strength_at_cycle(cycle, x, at_cycles):
    return cycle * x if cycle in at_cycles else 0


def compute_signal_strength(instructions, at_cycles):
    signal_strength = 0
    x = 1
    num_cycle = 1
    for instruction in instructions:

        if instruction == 'noop':
            signal_strength += compute_signal_strength_at_cycle(
                num_cycle, x, at_cycles)
            num_cycle += 1

        else:  # instruction is `addx <value>`
            add_to_x = int(re.search(r'-?\d+$', instruction)[0])
            signal_strength += compute_signal_strength_at_cycle(
                num_cycle, x, at_cycles)
            num_cycle += 1
            signal_strength += compute_signal_strength_at_cycle(
                num_cycle, x, at_cycles)
            num_cycle += 1
            x += add_to_x

    return signal_strength


if __name__ == '__main__':
    print(compute_signal_strength(
        instructions=get_instruction_lines('inputs/part_1_2.txt'),
        at_cycles=[20, 60, 100, 140, 180, 220]
    ))
