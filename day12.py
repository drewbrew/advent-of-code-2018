#!/usr/bin/env python

import collections

TEST_INPUT = """#..#.#..##......###...###..........."""
REAL_INPUT = """<paste starting inputs here>"""

REAL_CASES = """<paste cases here>""".split('\n')

TEST_CASES = """...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #""".split('\n')


def parse_cases(cases):
    parsed = set()
    for case in cases:
        state, result = case.split(' => ')
        if result == '#':
            parsed.add(state)
    return parsed


def next_generation(current, cases):
    start = min(current)
    end = max(current)
    result = set()
    for i in range(start - 3, end + 4):
        pattern = ''.join(
            '#' if i + k in current else '.' for k in range(-2, 3)
        )
        if pattern in cases:
            result.add(i)
    return result


def advance_generation(initial_condition, generations=20, cases=None):
    current = initial_condition.copy()
    turn = 0
    for i in range(generations):
        current = next_generation(current, cases)
    return current


def part_two(puzzle_input, generations, cases):
    last_sum = 0
    last_diff = 0
    diffs_equal = 0
    current = puzzle_input.copy()
    for generation in range(2000):
        current = next_generation(current, cases)
        current_sum = sum(current)
        current_diff = current_sum - last_sum
        if current_diff == last_diff:
            diffs_equal += 1
        last_sum = current_sum
        last_diff = current_diff
        if diffs_equal >= 100:
            print(
                f'found infinite loop after gen {generation},'
                f' puzzle increases by {last_diff}')
            generations_to_go = generations - generation - 1
            return last_sum + (last_diff * generations_to_go)


if __name__ == '__main__':
    test_input = set(
        index for index, value in enumerate(TEST_INPUT) if value == '#')
    test_gen20 = advance_generation(test_input, 20, parse_cases(TEST_CASES))
    assert sum(test_gen20) == 325, (list(sorted(test_gen20)), sum(test_gen20))
    real_input = set(
        index for index, value in enumerate(REAL_INPUT) if value == '#'
    )
    part_one = advance_generation(real_input, 20, parse_cases(REAL_CASES))
    print('Day 11, part 1 solution', sum(part_one))
    part_two_result = part_two(
        real_input, int(50e9), parse_cases(REAL_CASES))
    print('Day 11, part 2 solution', part_two_result)
