# Authored by Carlos Serra-Toro (https://carlosserratoro.com)
# See the file LICENSE for the licence
import os
import filesystem


def get_lines(source_file):
    with open(source_file) as f:
        for line in f:
            yield line.rstrip(os.linesep)


def build_fs(lines):
    """Build the filesystem"""
    fs = filesystem.FileSystem()
    for line in lines:
        if line[0] == '$' and line[2:4] == 'cd':  # Enter into a directory
            d_name = line[5:]
            if d_name == '..':
                fs.move_up()
            else:
                fs.move_to(d_name)
        elif line != '$ ls':
            if line[0] == 'd':  # Line starts with 'dir'
                d_name = line[4:]
                fs.add_directory(d_name)
            else:
                f_size, f_name = line.split(' ')
                fs.add_file(f_name, int(f_size))
    return fs


def part_1(fs):
    threshold = 100000
    sum_sizes = 0
    for node in fs:
        if node._is_dir and node._size < threshold:
            sum_sizes += node._size
    print('Part 1: Sum of sizes of dirs up to %d: %d.' %
          (threshold, sum_sizes))


def part_2(fs):
    total_space = 70000000
    required_unused_space = 30000000
    amount_to_free = required_unused_space - (total_space - fs._root._size)
    smallest_directory_size = total_space  # A value large enough
    for node in fs:
        if node._is_dir and node._size >= amount_to_free:
            if node._size < smallest_directory_size:
                smallest_directory_size = node._size
    print('Part 2: Total size of smallest directory to remove: %d' %
          smallest_directory_size)


if __name__ == '__main__':
    fs = build_fs(get_lines('inputs/part_1_2.txt'))
    print(fs)
    part_1(fs)
    part_2(fs)
