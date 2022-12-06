# Authored by Carlos Serra-Toro (https://carlosserratoro.com)
# See the file LICENSE for the licence
import os


START_OF_PACKET_SIZE = 4


def get_lines(source_file):
    with open(source_file) as f:
        for line in f:
            yield line.rstrip(os.linesep)


def _get_num_chars_to_process(line):
    """Get number of characters to find first start-of-packet"""
    i = 0
    while i < len(line):
        s = {line[i]}
        repeated_not_found = True
        j = 1
        while j < START_OF_PACKET_SIZE and repeated_not_found:
            if line[i+j] in s:
                repeated_not_found = False
            else:
                s.add(line[i+j])
            j += 1

        if repeated_not_found:
            return i + j
        else:
            i += 1

    return -1


def get_num_chars_to_process(lines):
    """Get number of characters to find first start-of-packet

    This is the multi line version, where we receive a stream
    of lines, each one being the stream of characters in a signal.
    """
    num_chars = []
    for line in lines:
        num_chars.append(_get_num_chars_to_process(line))
    return num_chars


if __name__ == '__main__':
    print(get_num_chars_to_process(get_lines('inputs/part_1_2.txt')))
