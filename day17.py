#!/usr/bin/env python
import enum
from typing import NamedTuple


TEST_INPUT = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504""".split('\n')

REAL_INPUT = """<paste inputs here>""".split('\n')


class Point(NamedTuple):
    x: int
    y: int


SPIGOT = Point(500, 0)


class SoilType(enum.Enum):
    DRY_SAND = enum.auto()
    CLAY = enum.auto()
    PREVIOUSLY_WET = enum.auto()
    WET = enum.auto()
    SPIGOT = enum.auto()


AT_REST_TYPES = {
    SoilType.CLAY,
    SoilType.WET,
}
PASS_THROUGH_TYPES = {
    SoilType.DRY_SAND,
    SoilType.PREVIOUSLY_WET,
}


def parse_input(input_lines):
    grid = {}
    for line in input_lines:
        first, second = line.split(', ')
        first_var, first_value = first.split('=')
        first_value = int(first_value)
        second_var, second_values = second.split('=')
        min_second, max_second = [int(i) for i in second_values.split('..')]
        for coord in range(min_second, max_second + 1):
            grid[Point(**{first_var: first_value, second_var: coord})] = \
                SoilType.CLAY
    x_list = sorted(grid, key=lambda pt: pt.x)
    min_x = x_list[0].x - 2
    max_x = x_list[-1].x + 3
    y_list = sorted(grid, key=lambda pt: pt.y)
    min_y = y_list[0].y
    max_y = y_list[-1].y + 1
    for x in range(min_x, max_x):
        for y in range(min_y, max_y):
            point = Point(x, y)
            if point not in grid:
                grid[point] = SoilType.DRY_SAND
    return grid


def produce_droplet():
    return SPIGOT


def place_droplet(starting_point, grid):
    y_list = sorted(grid, key=lambda k: k.y)
    min_y = y_list[0].y
    max_y = y_list[-1].y
    x_list = sorted(grid, key=lambda k: k.x)
    min_x = x_list[0].x
    max_x = x_list[-1].x
    if starting_point.y < min_y:
        starting_point = Point(y=min_y, x=starting_point.x)
    else:
        above = grid[Point(starting_point.x, starting_point.y - 1)]
        if above == SoilType.CLAY:
            print('bug found!')
            print(starting_point, above)
            display_grid(grid, starting_point)
            raise ValueError('oh no')
    while starting_point.y <= max_y:
        if starting_point.x == min_x:
            raise RuntimeError(starting_point)
        if grid[starting_point] == SoilType.WET:
            # already seen this branch
            return grid
        if grid[starting_point] == SoilType.DRY_SAND:
            # keep going down until we hit clay or wet sand at rest
            grid[starting_point] = SoilType.PREVIOUSLY_WET
            try:
                if grid[Point(starting_point.x, starting_point.y + 1)] \
                        not in AT_REST_TYPES:
                    # no match. move down
                    starting_point = Point(
                        starting_point.x, starting_point.y + 1)
                    continue
            except KeyError:
                return grid
            # we have a barrier beneath us. Need to see if we can fill in next
            # to it
            # look left and see if we have an edge to fall off
            left = None
            right = None
            left_cliff = False
            right_cliff = False
            for x in range(starting_point.x - 1, min_x, -1):
                neighbor = grid[Point(x, starting_point.y)]
                if neighbor == SoilType.CLAY:
                    left = Point(x, starting_point.y)
                    break
                below = grid[Point(x, starting_point.y + 1)]
                if below not in AT_REST_TYPES:
                    left = Point(x, starting_point.y)
                    left_cliff = True
                    break
            else:
                raise ValueError('Could not find left edge')
            for x in range(starting_point.x + 1, max_x):
                neighbor = grid[Point(x, starting_point.y)]
                if neighbor == SoilType.CLAY:
                    right = Point(x, starting_point.y)
                    break
                below = grid[Point(x, starting_point.y + 1)]
                if below not in AT_REST_TYPES:
                    right = Point(x, starting_point.y)
                    right_cliff = True
                    break
            else:
                raise ValueError('Could not find right edge')
            if not left_cliff and not right_cliff:
                # fill the entire row with water
                for x in range(left.x + 1, right.x):
                    grid[Point(x, starting_point.y)] = SoilType.WET
                # move up and restart the list
                starting_point = Point(starting_point.x, starting_point.y - 1)
                grid[starting_point] = SoilType.DRY_SAND
                continue
            # fill in the row
            for x in range(left.x + 1, right.x):
                grid[Point(x, starting_point.y)] = SoilType.PREVIOUSLY_WET
            if left_cliff:
                # continue from here going down
                place_droplet(left, grid)
            if right_cliff:
                # same
                place_droplet(right, grid)
            return grid
        starting_point = Point(starting_point.x, starting_point.y + 1)
    return grid


def display_soil_type(soil_type):
    return {
        SoilType.DRY_SAND: '.',
        SoilType.PREVIOUSLY_WET: '|',
        SoilType.WET: '~',
        SoilType.CLAY: '#',
        SoilType.SPIGOT: '+',
    }[soil_type]


def display_grid(grid, target=None):
    y_list = sorted(grid, key=lambda k: k.y)
    min_y = y_list[0].y
    max_y = y_list[-1].y
    x_list = sorted(grid, key=lambda k: k.x)
    min_x = x_list[0].x
    max_x = x_list[-1].x
    for y in range(min_y, max_y + 1):
        print(
            ''.join(
                display_soil_type(
                    grid[Point(x, y)],
                ) if Point(x, y) != target else '&'
                for x in range(min_x, max_x + 1)
            )
        )


if __name__ == '__main__':
    parsed = parse_input(TEST_INPUT)
    display_grid(parsed)
    place_droplet(produce_droplet(), parsed)
    display_grid(parsed)
    assert sum(1 for value in parsed.values() if value in {
        SoilType.PREVIOUSLY_WET, SoilType.WET
    }) == 57
    real_grid = parse_input(REAL_INPUT)
    place_droplet(produce_droplet(), real_grid)
    display_grid(real_grid)
    print(
        'Day 17, part 1 solution',
        sum(1 for value in real_grid.values() if value in {
            SoilType.PREVIOUSLY_WET, SoilType.WET
        }),
    )
    print(
        'Day 17, part 2 solution',
        sum(1 for value in real_grid.values() if value == SoilType.WET),
    )
