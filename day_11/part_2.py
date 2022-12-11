# Authored by Carlos Serra-Toro (https://carlosserratoro.com)
# See the file LICENSE for the licence
from monkeys import Monkeys


def main():
    monkeys = Monkeys()
    file_path = 'inputs/part_1_2.txt'
    print_process = True

    # Part 2 doesn't relax the worry *by default*, runs for 10000 rounds.
    #
    # The code (in my computer) started to run super slow at the
    # round ~700 or so. At first I thought it was because I was running
    # low on memory, but this wasn't the case after doing a memory inspection.
    # After using a code profiler, I found the bottleneck came because of
    # the arithmetic operations. Python has a big-number integrated by default,
    # thus I realised its slows operations were causing the overall slowdown.
    #
    # Thus I thought about a way of reducing the worry level in a way in which
    # it was still compatible with the test made by the monkeys. So I had to
    # relax the worry anyway, but in a way in which the divisions made by
    # the different monkeys didn't affect the final result. The easiest way
    # is to relax the worry by always using the remainder of the division of
    # the number by the product of all the divisors, that way we are sure we
    # are mapping any arbitrarily large number to a fixed domain range, the
    # divisions of which are compatible with the original non-mapped values.
    monkeys.build_from_file(file_path, print_after_build=print_process)

    def relax_worry(worry_level):
        """Relax the worry level

        Here, being all divisors prime numbers, the multiplication
        of all the numbers yields a divisor that is also the LCD.
        """
        divisor = 1
        for monkey in monkeys:
            divisor *= monkey.divisible_by
        return worry_level % divisor

    monkeys.process_items(
        num_rounds=10000,
        relax_func=relax_worry,
        show_progress=print_process)
    print('Part 2: ', monkeys.get_level_of_business())


if __name__ == '__main__':
    main()
