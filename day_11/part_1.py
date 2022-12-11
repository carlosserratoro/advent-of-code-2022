# Authored by Carlos Serra-Toro (https://carlosserratoro.com)
# See the file LICENSE for the licence
from monkeys import Monkeys


def main():
    monkeys = Monkeys()
    file_path = 'inputs/part_1_2.txt'
    print_process = True

    # Part 1 relaxes the worry, runs for 20 rounds
    monkeys.build_from_file(file_path, print_after_build=print_process)

    def relax_worry(worry_level):
        return worry_level // 3

    monkeys.process_items(
        num_rounds=20,
        relax_func=relax_worry,
        show_progress=print_process)
    print('Part 1: ', monkeys.get_level_of_business())


if __name__ == '__main__':
    main()
