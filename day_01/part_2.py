# Authored by Carlos Serra-Toro (https://carlosserratoro.com)
# See the file LICENSE for the licence
import array
import os


def get_calories_data(source_file):
    with open(source_file) as f:
        for line in f:
            yield line.rstrip(os.linesep)


def get_top_three_max_calories(calories_data):
    """Get the sum of the top-three maximum amount of calories.

    It receives a stream of calories data and checks,
    once it has found a new chunk of calories, if its
    sum is among the three maximum quantities that we
    have found till now, and if so updates.
    """

    # Here the key is to not load the whole file into
    # memory, but to process the lines one by one, because
    # we don't know how long the input can be.

    # Here it is key to find if we have found a new top-three
    # quickly. To do so we keep the array in order so that just
    # checking for the first element in the array is enough
    # to know if we have a new maximum. Keeping it sorted is
    # trivial being a 3-element array.

    top_3 = array.array('L', [0, 0, 0])

    current_elf_calories = 0
    for calories in calories_data:
        if calories:
            current_elf_calories += int(calories)
        else:
            if current_elf_calories > top_3[0]:
                # Float the new max till sorting is kept
                top_3[0] = current_elf_calories
                i = 1
                while i < len(top_3) and top_3[i-1] > top_3[i]:
                    top_3[i], top_3[i-1] = top_3[i-1], top_3[i]
                    i += 1

            current_elf_calories = 0
    return sum(top_3)


if __name__ == '__main__':
    print(get_top_three_max_calories(get_calories_data('inputs/part_1.txt')))
