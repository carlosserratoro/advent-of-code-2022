# Authored by Carlos Serra-Toro (https://carlosserratoro.com)
# See the file LICENSE for the licence
import array
import os


# Items are identified by a letter in [A-Za-z]
NUM_ITEMS = (ord('Z') - ord('A') + 1) * 2


def get_rucksacks_data(source_file):
    with open(source_file) as f:
        for line in f:
            yield line.rstrip(os.linesep)


def letter_to_index(letter):
    """Given a letter in [A-Za-z] return a unique indexing position"""
    if letter <= 'Z':
        index = ord(letter) - ord('A')
    else:
        offset_uppercase_z = ord('Z') - ord('A') + 1
        index = ord(letter) - ord('a') + offset_uppercase_z
    return index


def letter_to_priority(letter):
    if letter <= 'Z':  # letter in [A-Z]
        priority = ord(letter) - ord('A') + NUM_ITEMS//2 + 1
    else:  # letter in [a-z]
        priority = ord(letter) - ord('a') + 1
    return priority


def get_sum_of_priorities(rucksacks_data):
    """Get sum of priorities for the item duplicated on both compartments"""

    sum_of_priorities = 0

    for rucksack in rucksacks_data:
        item_count = array.array('b', (0 for _ in range(NUM_ITEMS)))

        # Find which items we have in the first compartment, which is
        # in the first half of the rucksack.
        i = 0
        while i < len(rucksack) // 2:
            letter = rucksack[i]
            item_count[letter_to_index(letter)] += 1
            i += 1

        # Iterate through the second compartment, which is in the second
        # half of the rucksack, to find the item that is also in the first
        # compartment.
        shared_item_found = False
        while i < len(rucksack) and not shared_item_found:
            letter = rucksack[i]
            if item_count[letter_to_index(letter)] > 0:  # Item found.
                sum_of_priorities += letter_to_priority(letter)
                shared_item_found = True
            i += 1

    return sum_of_priorities


if __name__ == '__main__':
    print(get_sum_of_priorities(get_rucksacks_data('inputs/part_1_2.txt')))
