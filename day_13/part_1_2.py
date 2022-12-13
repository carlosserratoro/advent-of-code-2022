# Authored by Carlos Serra-Toro (https://carlosserratoro.com)
# See the file LICENSE for the licence
import os


def get_pairs_of_lists(file_path):
    """Return tuples (num-pair, pair-of-lists)"""
    with open(file_path) as f:
        num_pair = 1
        pair = []
        for line in f:
            if line != os.linesep:
                pair.append(eval(line))
            if len(pair) == 2:
                yield num_pair, pair
                pair = []
                num_pair += 1


def cmp(l1, l2):
    """Compare the two lists according to AoC Day 13

    Returns +1 if l1 is smaller, thus are in right order.
    Returns -1 if l2 is smaller, thus are in wrong order.
    Returns 0 if l1 and l2 are equal.
    """
    i = 0
    res = 0
    while i < len(l1) and i < len(l2) and res == 0:
        if isinstance(l1[i], int) and isinstance(l2[i], int):
            if l1[i] < l2[i]:
                res = +1
            elif l1[i] > l2[i]:
                res = -1
            else:  # if l1[i] == l2[i]:
                res = 0
        elif isinstance(l1[i], int) and isinstance(l2[i], list):
            res = cmp([l1[i]], l2[i])
        elif isinstance(l1[i], list) and isinstance(l2[i], int):
            res = cmp(l1[i], [l2[i]])
        elif isinstance(l1[i], list) and isinstance(l2[i], list):
            res = cmp(l1[i], l2[i])
        else:
            raise ValueError(
                'Bad input. We expect lists of integers/lists, recursively.')
        i += 1

    if res == 0:
        if i == len(l1) and i < len(l2):
            res = +1
        elif i < len(l1) and i == len(l2):
            res = -1

    return res


class Packet:
    """Wraps a list as a packet

    This class is created just for convenience, to be
    able to sort easily a list of packets by reusing `cmp()`
    in Part 2.
    """
    def __init__(self, content):
        self.content = content

    def __lt__(self, other):
        return cmp(self.content, other.content) == -1

    def __repr__(self):
        return str(self.content)

    def __eq__(self, other):
        return self.content == other.content


def part_1(pairs_data):
    """Return the solution for the Part 1"""
    pairs_in_right_order = 0
    for num_pair, pair in pairs_data:
        if cmp(pair[0], pair[1]) == +1:
            pairs_in_right_order += num_pair
    return pairs_in_right_order


def part_2(pairs_data):
    """Return the solution for the Part 2"""
    packet_divider_2 = Packet([[2]])
    packet_divider_6 = Packet([[6]])
    all_packets = [packet_divider_2, packet_divider_6]
    for _, pair in pairs_data:
        all_packets.append(Packet(pair[0]))
        all_packets.append(Packet(pair[1]))
    all_packets.sort(reverse=True)

    decoder_keys = [0, 0]
    i = 0
    while (
        i < len(all_packets)
        and (decoder_keys[0] == 0 or decoder_keys[1] == 0)
    ):
        if all_packets[i] == packet_divider_2:
            decoder_keys[0] = i + 1
        elif all_packets[i] == packet_divider_6:
            decoder_keys[1] = i + 1
        i += 1
    return decoder_keys[0] * decoder_keys[1]


if __name__ == '__main__':
    # Assertions and solution for Part 1:
    assert +1 == cmp([1, 1, 3, 1, 1], [1, 1, 5, 1, 1])
    assert +1 == cmp([[1], [2, 3, 4]], [[1], 4])
    assert -1 == cmp([9], [[8, 7, 6]])
    assert +1 == cmp([[4, 4], 4, 4], [[4, 4], 4, 4, 4])
    assert -1 == cmp([7, 7, 7, 7], [7, 7, 7])
    assert +1 == cmp([], [3])
    assert -1 == cmp([[[]]], [[]])
    assert -1 == cmp([1, [2, [3, [4, [5, 6, 7]]]], 8, 9],
                     [1, [2, [3, [4, [5, 6, 0]]]], 8, 9])

    assert 13 == part_1(get_pairs_of_lists('inputs/part_1_2_test.txt'))

    print('Part 1: ', part_1(get_pairs_of_lists('inputs/part_1_2.txt')))
    assert 5366 == part_1(get_pairs_of_lists('inputs/part_1_2.txt'))

    # Assertions and solution for Part 2:
    assert 140 == part_2(get_pairs_of_lists('inputs/part_1_2_test.txt'))

    print('Part 2: ', part_2(get_pairs_of_lists('inputs/part_1_2.txt')))
    assert 23391 == part_2(get_pairs_of_lists('inputs/part_1_2.txt'))
