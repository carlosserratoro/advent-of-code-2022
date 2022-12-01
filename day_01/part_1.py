# Authored by Carlos Serra-Toro (https://carlosserratoro.com)
# See the file LICENSE for the licence
import os


def get_calories_data(source_file):
    with open(source_file) as f:
        for line in f:
            yield line.rstrip(os.linesep)


def get_max_calories(calories_data):
    """Get the maximum amount of calories.

    It receives a stream of calories data and checks,
    once it has found a new chunk of calories, if its
    sum is bigger than the maximum value that we had,
    and if so updates.
    """

    # Here the key is to not load the whole file into
    # memory, but to process the lines one by one, because
    # we don't know how long the input can be.

    max_calories = 0
    current_elf_calories = 0
    for calories in calories_data:
        if calories:
            current_elf_calories += int(calories)
        else:
            if current_elf_calories > max_calories:
                max_calories = current_elf_calories
            current_elf_calories = 0
    return max_calories


if __name__ == '__main__':
    print(get_max_calories(get_calories_data('inputs/part_1.txt')))
