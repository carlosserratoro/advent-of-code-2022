# Authored by Carlos Serra-Toro (https://carlosserratoro.com)
# See the file LICENSE for the licence
import array
import os


# Items are identified by a letter in [A-Za-z]
NUM_ITEMS = (ord('Z') - ord('A') + 1) * 2


# Rucksacks per group of elves
RUCKSACKS_PER_GROUP = 3


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


def get_sum_of_badges(rucksacks_data):
    """Get sum of priorities for the badges of each group of elves"""

    sum_of_badges = 0
    item_count = array.array('b', (0 for _ in range(NUM_ITEMS)))

    for rucksack_no, rucksack in enumerate(rucksacks_data):
        rucksack_in_group_no = rucksack_no % RUCKSACKS_PER_GROUP

        if rucksack_no and rucksack_in_group_no == 0:
            # A new group of rucksacks starts, so clear out the values.
            for i in range(NUM_ITEMS):
                item_count[i] = 0

        # All but the last rucksack per group simply marks if we have
        # seen that item on that rucksack. So first rucksack adds 1,
        # second rucksack adds 1 only if it was already in the first
        # rucksack (thus resulting into a result of 2) and so on, till
        # the last rucksack that stops as soon as the result after the
        # add is equal to the amount of rucksacks per group, because
        # that means the item has been in all the rucksacks seen.
        if rucksack_in_group_no != RUCKSACKS_PER_GROUP - 1:
            for letter in rucksack:
                letter_count = item_count[letter_to_index(letter)]
                if letter_count == rucksack_in_group_no:
                    item_count[letter_to_index(letter)] += 1

        else:  # if rucksack_no == RUCKSACKS_PER_GROUP - 1:
            badge_found = False
            i = 0
            while i < len(rucksack) and not badge_found:
                letter = rucksack[i]
                letter_count = item_count[letter_to_index(letter)]
                if letter_count == rucksack_in_group_no:
                    sum_of_badges += letter_to_priority(letter)
                    badge_found = True
                i += 1

    return sum_of_badges


if __name__ == '__main__':
    print(get_sum_of_badges(get_rucksacks_data('inputs/part_1_2.txt')))
