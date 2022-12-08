# Authored by Carlos Serra-Toro (https://carlosserratoro.com)
# See the file LICENSE for the licence
import os
import array


def get_lines(source_file):
    with open(source_file) as f:
        for line in f:
            yield line.rstrip(os.linesep)


def get_lines_reversed(source_file, num_lines):
    with open(source_file) as f:
        len_line = len(f.readline())
        f.seek(0, 0)
        for num_line in range(num_lines-1, -1, -1):
            f.seek(num_line * len_line, 0)
            yield f.readline().rstrip(os.linesep)


def get_num_trees_seen(file_path):
    """Get the number of trees that can be seen from any side

    I'm doing this in a space and time efficient way, where I
    don't build the whole matrix but instead read the file twice:
    one from top-to-bottom, and one from bottom-to-top.
    """
    trees = set()

    num_lines_in_file = 0
    for row_no, line in enumerate(get_lines(file_path)):
        num_lines_in_file += 1
        if row_no == 0:
            # If it's the first row, create an empty skyline that
            # can be for sure updated in the first row, so that
            # all the trees in the front row are added as visible
            # trees.
            skyline_top = array.array('b', (-1 for _ in line))

        # Store the portion of the skyline of the forest as would
        # be seen if we scanned using columns, from left to right
        # and from right to left.
        skyline_left = -1
        skyline_right = -1

        array_line = array.array('b', (int(c) for c in line))
        for col_no in range(len(array_line)):

            # If we see a taller from the top of the forest, then update
            # the skyline and add that tree to the list of seen trees.
            if array_line[col_no] > skyline_top[col_no]:
                skyline_top[col_no] = array_line[col_no]
                trees.add((row_no, col_no))

            # If we see a taller tree from the left of the forest,
            # then update the skyline and add that tree to the list
            # of seen trees.
            if array_line[col_no] > skyline_left:
                skyline_left = array_line[col_no]
                trees.add((row_no, col_no))

        # If we see a taller tree from the right of the forest,
        # then update the skyline and add that tree to the list
        # of seen trees.
        for col_no in range(len(array_line) - 1, -1, -1):
            if array_line[col_no] > skyline_right:
                skyline_right = array_line[col_no]
                trees.add((row_no, col_no))

            # If we found from the right the skyline from the left
            # then we can stop here, because we won't see any further.
            if array_line[col_no] == skyline_left:
                break

    # Scan the file from bottom to top, to determine which trees
    # are seen from the bottom of the forest. The algorithm is the
    # same than for the case in which we scanned from top to bottom.
    for row_from_bottom_no, line in enumerate(
            get_lines_reversed(file_path, num_lines_in_file)
    ):
        if row_from_bottom_no == 0:
            skyline_bottom = array.array('b', (-1 for _ in line))
        array_line = array.array('b', (int(c) for c in line))
        for col_no in range(len(array_line)):
            if array_line[col_no] > skyline_bottom[col_no]:
                skyline_bottom[col_no] = array_line[col_no]
                actual_row = num_lines_in_file - row_from_bottom_no - 1
                trees.add((actual_row, col_no))

    return len(trees)


if __name__ == '__main__':
    print(get_num_trees_seen('inputs/part_1_2.txt'))
