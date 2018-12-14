#!/usr/bin/env python

STARTING_CONDITION = [int(i) for i in '3 7'.split()]
TEST_CASES = """(3)[7]
(3)[7] 1  0
 3  7  1 [0](1) 0
 3  7  1  0 [1] 0 (1)
(3) 7  1  0  1  0 [1] 2
 3  7  1  0 (1) 0  1  2 [4]
 3  7  1 [0] 1  0 (1) 2  4  5
 3  7  1  0 [1] 0  1  2 (4) 5  1
 3 (7) 1  0  1  0 [1] 2  4  5  1  5
 3  7  1  0  1  0  1  2 [4](5) 1  5  8
 3 (7) 1  0  1  0  1  2  4  5  1  5  8 [9]
 3  7  1  0  1  0  1 [2] 4 (5) 1  5  8  9  1  6
 3  7  1  0  1  0  1  2  4  5 [1] 5  8  9  1 (6) 7
 3  7  1  0 (1) 0  1  2  4  5  1  5 [8] 9  1  6  7  7
 3  7 [1] 0  1  0 (1) 2  4  5  1  5  8  9  1  6  7  7  9
 3  7  1  0 [1] 0  1  2 (4) 5  1  5  8  9  1  6  7  7  9  2""".split('\n')


# Paste input here
REAL_INPUT = 0

TARGETS = {
    9: '5158916779',
    5: '0124515891',
    18: '9251071085',
    2018: '5941429882',
}


TEST_CASES_PARSED = []

for line in TEST_CASES:
    line = line.replace('](', '  ').replace(')[', '  ')
    for special in '([])':
        line = line.replace(special, ' ')
    TEST_CASES_PARSED.append(line.split(' '))


def make_recipes(recipes, elf1, elf2):
    elf1_score = recipes[elf1]
    elf2_score = recipes[elf2]
    new_score = elf1_score + elf2_score
    recipes += [int(i) for i in str(new_score)]
    elf1_new_index = (elf1 + elf1_score + 1) % len(recipes)
    elf2_new_index = (elf2 + elf2_score + 1) % len(recipes)
    return elf1_new_index, elf2_new_index


def run_puzzle(puzzle_input, recipe_target, next_recipes=10):
    elf1 = 0
    elf2 = 1
    total_recipes = 0
    puzzle = puzzle_input[:]
    iterations = 0
    while len(puzzle) < recipe_target + next_recipes:
        if puzzle_input == TEST_CASES:
            if iterations < len(TEST_CASES_PARSED):
                assert puzzle == TEST_CASES_PARSED[iteration], (
                    puzzle, TEST_CASES_PARSED[iteration], iterations)
            for length, value in TARGETS.items():
                if len(puzzle) >= length + 10:
                    next_ten = puzzle[length:length + 10]
                    assert ''.join(str(i) for i in next_ten) == value, (
                        length, next_ten, value, puzzle)
        elf1, elf2 = make_recipes(puzzle, elf1, elf2)
        iterations += 1
    return ''.join(
        str(i) for i in puzzle[recipe_target:recipe_target + next_recipes])


def part_two(puzzle_input, target):
    elf1 = 0
    elf2 = 1
    puzzle = puzzle_input[:]
    while True:
        elf1, elf2 = make_recipes(puzzle, elf1, elf2)
        if len(puzzle) > len(target):
            puzzle_string = ''.join(str(i) for i in puzzle[-20:])
            if target in puzzle_string:
                index = puzzle_string.index(target)
                if len(puzzle) < 20:
                    return index
                return index + len(puzzle) - 20


if __name__ == '__main__':
    print('running tests')
    run_puzzle(STARTING_CONDITION, 2018, 10)
    assert part_two(STARTING_CONDITION, '51589') == 9
    assert part_two(STARTING_CONDITION, '01245') == 5
    assert part_two(STARTING_CONDITION, '92510') == 18
    assert part_two(STARTING_CONDITION, '59414') == 2018
    print('tests passed')
    print(
        'Day 14, part 1 solution',
        run_puzzle(STARTING_CONDITION, REAL_INPUT, 10))
    print(
        'Day 14, part 2 solution',
        part_two(STARTING_CONDITION, str(REAL_INPUT)))
