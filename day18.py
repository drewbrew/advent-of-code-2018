#!/usr/bin/env python

"""An open acre will become filled with trees if three or more
adjacent acres contained trees. Otherwise, nothing happens.

An acre filled with trees will become a lumberyard if three or
more adjacent acres were lumberyards. Otherwise, nothing happens.

An acre containing a lumberyard will remain a lumberyard if it was
adjacent to at least one other lumberyard and at least one acre containing
trees. Otherwise, it becomes open."""

from collections import deque

TEST_INPUT = """.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.""".split('\n')


TEST_GRID_ONE_MIN = """.......##.
......|###
.|..|...#.
..|#||...#
..##||.|#|
...#||||..
||...|||..
|||||.||.|
||||||||||
....||..|.""".split('\n')

TEST_GRID_TEN_MIN = """.||##.....
||###.....
||##......
|##.....##
|##.....##
|##....##|
||##.####|
||#####|||
||||#|||||
||||||||||""".split('\n')


REAL_INPUT = """<paste inputs here>""".split('\n')


def parse_input(input_lines):
    grid = []
    for line in input_lines:
        line_list = [
            i for i in line
        ]
        grid.append(line_list)
    return grid


def action_at_char(point, neighbors):
    if point == '.':
        if sum(1 for i in neighbors if i == '|') >= 3:
            # open becomes tree if 3+ neighbors are trees
            return '|'
    elif point == '|':
        if sum(1 for i in neighbors if i == '#') >= 3:
            # tree becomes lumberyard if 3+ neighbors are lumberyards
            return '#'
    elif point == '#':
        if sum(1 for i in neighbors if i == '#') >= 1 and \
                sum(1 for i in neighbors if i == '|') >= 1:
            # lumberyard only stays lumberyard if there's at least one of each
            # of tree and lumberyard adjacent
            return '#'
        # otherwise it's open
        return '.'
    # stays as is
    return point


def advance_turn(grid):
    result = []
    y = 0
    before_row = []
    after_row = []
    current_row = []
    while y < len(grid):
        if not before_row:
            # first iteration
            before_row = ['.'] * len(grid[0])
            current_row = grid[y]
            after_row = grid[y + 1]
        else:
            before_row = current_row
            current_row = after_row
            try:
                after_row = grid[y + 1]
            except IndexError:
                after_row = ['.'] * len(current_row)
        x = 0
        last_chars = []
        current_chars = []
        next_chars = []
        result_row = []
        active_char = ''
        while x < len(current_row):
            if not last_chars:
                # first one. Prepopulate last chars with open spaces
                last_chars = ['.'] * 3
                current_chars = [
                    before_row[x], after_row[x],
                ]
                active_char = current_row[x]
                next_chars = [
                    before_row[x + 1], current_row[x + 1], after_row[x + 1],
                ]
            else:
                last_chars = current_chars + [active_char]
                active_char = next_chars[1]
                current_chars = [next_chars[0], next_chars[2]]
                try:
                    next_chars = [
                        before_row[x + 1], current_row[x + 1],
                        after_row[x + 1],
                    ]
                except IndexError:
                    next_chars = ['.'] * 3
            result_row.append(
                action_at_char(
                    active_char, current_chars + next_chars + last_chars,
                )
            )
            x += 1
        result.append(result_row)
        y += 1
    return result


def part_two(grid, iterations=1000000000):
    grids_seen = []
    iteration = 1
    while iteration < iterations:
        if grid in grids_seen:
            first_repeat_index = grids_seen.index(grid)
            print(f"Found {iteration} as a repeat of {first_repeat_index + 1}")
            period = iteration - (first_repeat_index + 1)
            print(period)
            repeating = grids_seen[first_repeat_index:]
            # NOTE: I know there is a better way to do this, but my math just
            # wouldn't check out cleanly. Extrapolation it is.
            assert grid == repeating[0]
            assert advance_turn(grid) == repeating[1]
            while len(grids_seen) < iterations:
                grids_seen += repeating
            return grids_seen[iterations]

        grids_seen.append(grid)
        grid = advance_turn(grid)
        iteration += 1
    raise ValueError('OH NO')


def resources(grid):
    trees = sum(1 for line in grid for char in line if char == '|')
    lumberyards = sum(
        1 for line in grid for char in line if char == '#')
    return trees * lumberyards


if __name__ == '__main__':
    test_grid = parse_input(TEST_INPUT)
    print('\n'.join(''.join(i for i in row) for row in test_grid))
    one_min = advance_turn(test_grid)
    assert [''.join(i) for i in one_min] == TEST_GRID_ONE_MIN, [
        ''.join(i) for i in one_min]
    next_grid = one_min
    for i in range(9):
        next_grid = advance_turn(next_grid)
    assert [''.join(i) for i in next_grid] == TEST_GRID_TEN_MIN, [
        ''.join(i) for i in next_grid]
    trees = sum(1 for line in next_grid for char in line if char == '|')
    lumberyards = sum(1 for line in next_grid for char in line if char == '#')
    assert trees == 37, trees
    assert lumberyards == 31, lumberyards
    assert resources(next_grid) == 37 * 31
    print('tests passed')
    real_grid = parse_input(REAL_INPUT)
    current_grid = real_grid[:]
    for i in range(10):
        current_grid = advance_turn(current_grid)
    print('Day 18, part 1 solution', resources(current_grid))
    current_grid = parse_input(REAL_INPUT)
    current_grid = part_two(current_grid)
    print('Day 18, part 2 solution', resources(current_grid))
