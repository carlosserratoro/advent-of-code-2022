# Authored by Carlos Serra-Toro (https://carlosserratoro.com)
# See the file LICENSE for the licence
import os
import re
from collections import deque


REGEX_NUM = re.compile(r'\d+')
REGEX_OPERATION_LINE = re.compile(r'Operation: new = (?P<eval_operation>.*)')
REGEX_CONDITION = re.compile(r'If (?P<condition>\w+):.+(?P<monkey>\d+)')


class Monkeys:
    def __init__(self):
        self._monkeys = []

    def __str__(self):
        o = []
        for monkey in self._monkeys:
            o.extend([
                'Monkey %d:' % monkey.number,
                '  Starting items: %s' % ', '.join(map(str, monkey.items)),
                '  Operation: new = %s' % monkey.eval_operation,
                '  Test: divisible by %d' % monkey.divisible_by,
                '    If true: throw to monkey %d' % monkey.if_true_throw_to,
                '    If false: throw to monkey %d' % monkey.if_false_throw_to,
                '',
            ])
        return os.linesep.join(o)

    def __iter__(self):
        for m in self._monkeys:
            yield m

    def build_from_file(self, file_path, print_after_build=False):
        """Build the monkey data structure"""

        # The lines per monkey in the input file (last one has actually
        # one less, but doesn't affect us)
        lines_per_monkey = 7

        with open(file_path) as f:
            for line_no, line in enumerate(f):

                # Header for the monkey number
                if line_no % lines_per_monkey == 0:
                    num_monkey = int(re.search(REGEX_NUM, line)[0])
                    self._monkeys.append(Monkey(num_monkey))

                # Line for the starting items
                elif line_no % lines_per_monkey == 1:
                    items = []
                    for item in re.finditer(REGEX_NUM, line):
                        items.append(int(item[0]))
                    self._monkeys[-1].items.extend(items)

                # Line for the operation, in the form  `new = old OP NUM`
                elif line_no % lines_per_monkey == 2:
                    m = re.search(REGEX_OPERATION_LINE, line)
                    self._monkeys[-1].eval_operation = m['eval_operation']

                # Line for the test condition
                elif line_no % lines_per_monkey == 3:
                    divisible_by = int(re.search(REGEX_NUM, line)[0])
                    self._monkeys[-1].divisible_by = divisible_by

                # Lines for the true/false conditions
                elif line_no % lines_per_monkey in (4, 5):
                    m = re.search(REGEX_CONDITION, line)
                    if m['condition'] == 'true':
                        self._monkeys[-1].if_true_throw_to = int(m['monkey'])
                    else:  # if m['condition'] == 'false':
                        self._monkeys[-1].if_false_throw_to = int(m['monkey'])

        if print_after_build:
            print(self._monkeys)

    def process_items(self, num_rounds, relax_func, show_progress=False):
        """Monkeys process items in order, a number of rounds"""
        for round_no in range(num_rounds):
            for monkey in self._monkeys:
                throws = monkey.get_throws(relax_func)
                for dest_monkey, worry_level in throws:
                    self._monkeys[dest_monkey].items.append(worry_level)

            if show_progress:
                print()
                print('Round %d' % (round_no + 1))
                for monkey in self._monkeys:
                    print('Monkey %d [inspected %d]: %s' %
                          (monkey.number,
                           monkey.num_items_inspected,
                           ', '.join(map(str, monkey.items))))

    def get_level_of_business(self, num_monkeys=2):
        """Multiply the items processed by the N most active monkeys"""
        level = 1
        for monkey_no, monkey in enumerate(
            sorted(
                self._monkeys,
                key=lambda m: m.num_items_inspected,
                reverse=True
            )
        ):
            if monkey_no >= num_monkeys:
                break
            level *= monkey.num_items_inspected
        return level


class Monkey:
    def __init__(self, number):
        self.number = number
        self.items = deque()
        self.eval_operation = None
        self.divisible_by = None
        self.if_true_throw_to = None
        self.if_false_throw_to = None
        self.num_items_inspected = 0

    def get_throws(self, relax_func):
        throws = []
        while self.items:
            item = self.items.popleft()
            self.num_items_inspected += 1
            worry_level = eval(self.eval_operation, {'old': item})
            worry_level = relax_func(worry_level)
            throw_to = (
                self.if_true_throw_to if worry_level % self.divisible_by == 0
                else self.if_false_throw_to)
            throws.append((throw_to, worry_level))
        return throws
