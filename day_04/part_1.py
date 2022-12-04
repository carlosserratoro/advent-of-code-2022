# Authored by Carlos Serra-Toro (https://carlosserratoro.com)
# See the file LICENSE for the licence
import os


def get_ranges_data(source_file):
    with open(source_file) as f:
        for line in f:
            ranges_str = line.rstrip(os.linesep).split(',')
            first_range = tuple(map(int, ranges_str[0].split('-')))
            second_range = tuple(map(int, ranges_str[1].split('-')))
            yield first_range, second_range


def ranges_fully_overlap(a, b):
    return (a[0] <= b[0] and a[1] >= b[1]) or (b[0] <= a[0] and b[1] >= a[1])


def get_num_of_fully_overlaps(ranges_data):
    res = 0
    for first_range, second_range in ranges_data:
        res += ranges_fully_overlap(first_range, second_range)
    return res


if __name__ == '__main__':
    print(get_num_of_fully_overlaps(get_ranges_data('inputs/part_1_2.txt')))
