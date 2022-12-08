# Authored by Carlos Serra-Toro (https://carlosserratoro.com)
# See the file LICENSE for the licence
import os
import array


def get_lines(source_file):
    with open(source_file) as f:
        for line in f:
            yield line.rstrip(os.linesep)


def get_scenic_score(forest, tree_position):
    """Get the scenic score for a tree on the forest"""
    seen_left = 0
    seen_right = 0
    seen_up = 0
    seen_down = 0

    tree_row, tree_col = tree_position
    tree_height = forest[tree_row][tree_col]

    keep_looking_up = True
    row_it = tree_row - 1
    while keep_looking_up:
        other_tree_height = forest[row_it][tree_col]
        if other_tree_height <= tree_height:
            seen_up += 1
        row_it -= 1
        keep_looking_up = (
            row_it >= 0
            and other_tree_height < tree_height)

    keep_looking_down = True
    row_it = tree_row + 1
    while keep_looking_down:
        other_tree_height = forest[row_it][tree_col]
        seen_down += 1
        row_it += 1
        keep_looking_down = (
            row_it < len(forest)
            and other_tree_height < tree_height)

    keep_looking_left = True
    col_it = tree_col - 1
    while keep_looking_left:
        other_tree_height = forest[tree_row][col_it]
        seen_left += 1
        col_it -= 1
        keep_looking_left = (
            col_it >= 0
            and other_tree_height < tree_height)

    keep_looking_right = True
    col_it = tree_col + 1
    while keep_looking_right:
        other_tree_height = forest[tree_row][col_it]
        seen_right += 1
        col_it += 1
        keep_looking_right = (
            col_it < len(forest[0])
            and other_tree_height < tree_height)

    return seen_left * seen_right * seen_up * seen_down


def get_highest_scenic_score(lines):
    """Get the highest scenic score for any tree in the forest"""

    # In this case I am loading all the forest into memory.
    forest = []
    for line in lines:
        forest.append(array.array('B', (int(c) for c in line)))

    highest_scenic_score = -1
    num_cols, num_rows = len(forest), len(forest[0])
    for row_no in range(1, num_rows - 1):
        for col_no in range(1, num_cols - 1):
            scenic_score = get_scenic_score(forest, (row_no, col_no))
            if scenic_score > highest_scenic_score:
                highest_scenic_score = scenic_score
    return highest_scenic_score


if __name__ == '__main__':
    print(get_highest_scenic_score(get_lines('inputs/part_1_2.txt')))
