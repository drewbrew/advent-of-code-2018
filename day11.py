#!/usr/bin/env python
from functools import partial
import numpy
# replace with your number
SERIAL_NUMBER = 0

TEST_INPUTS = {
    (122, 79, 57): -5,
    (217, 196, 39): 0,
    (101, 153, 71): 4,
}
TEST_POWERS = {
    18: (33, 45, 29),
    42: (21, 61, 30),
}
PART_TWO_POWERS = {
    18: (90, 269, 16, 113),
    42: (232, 251, 12, 119),
}


def power_level(x, y, serial_number, increment=False):
    """Find the fuel cell's rack ID, which is its X coordinate plus 10.
    Begin with a power level of the rack ID times the Y coordinate.
    Increase the power level by the value of the grid serial number
        (your puzzle input).
    Set the power level to itself multiplied by the rack ID.
    Keep only the hundreds digit of the power level
        (so 12345 becomes 3; numbers with no hundreds digit become 0).
    Subtract 5 from the power level."""
    if increment:
        # for zero-based numbering (such as with numpy), we need to increase
        # both coordinates by 1 to get the right result
        x += 1
        y += 1
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial_number
    power_level *= rack_id
    hundreds_digit = int(power_level / 100) % 10
    if power_level < 0:
        # get it back to negative
        hundreds_digit -= 10
    hundreds_digit -= 5
    return hundreds_digit


def populate_grid(serial_number, max_x=300, max_y=300):
    vector_power_level = numpy.vectorize(
        partial(power_level, serial_number=serial_number, increment=True)
    )
    grid = numpy.fromfunction(vector_power_level, (max_x, max_y))
    return grid


def max_power_area(grid, size=3):
    areas = sum(
        # the or None is there so we can catch the last column/row cleanly
        grid[x: x - size + 1 or None, y: y - size + 1 or None]
        for x in range(size)
        for y in range(size)
    )
    biggest = int(areas.max())
    location = numpy.where(areas == biggest)
    return (location[0][0] + 1, location[1][0] + 1), biggest


if __name__ == '__main__':
    for (x, y, serial_number), result in TEST_INPUTS.items():
        test_power = power_level(x, y, serial_number)
        assert test_power == result, (x, y, serial_number, result, test_power)
    for serial_number, (x, y, power) in TEST_POWERS.items():
        test_grid = populate_grid(serial_number)
        (test_x, test_y), test_power = max_power_area(test_grid)
        assert (test_x, test_y, test_power) == (x, y, power), (
            (test_x, test_y, test_power), (x, y, power))
    for serial_number, (x, y, size, power) in PART_TWO_POWERS.items():
        print('testing', serial_number)
        test_grid = populate_grid(serial_number)
        max_power = 0
        max_x = 0
        max_y = 0
        max_size = 0
        for test_size in range(1, 30):
            (test_x, test_y), test_power = max_power_area(test_grid, test_size)
            if test_power > max_power:
                max_power = test_power
                max_x = test_x
                max_y = test_y
                max_size = test_size
            print(f'got {test_power} for {test_x},{test_y}, size {size}')
        assert (max_x, max_y, max_size, max_power) == (x, y, size, power), \
            ((max_x, max_y, max_size, max_power), (x, y, size, power))
    real_grid = populate_grid(SERIAL_NUMBER)
    (x, y), power = max_power_area(real_grid)
    print(f'Day 11, part 1 solution: {x},{y} power {power}')
    max_power = 0
    max_x = 0
    max_y = 0
    max_size = 0
    for size in range(1, 30):
        (test_x, test_y), test_power = max_power_area(real_grid, size)
        print(f'got {test_power} for {test_x},{test_y}, size {size}')
        if test_power > max_power:
            max_power = test_power
            max_x = test_x
            max_y = test_y
            max_size = size
    print(
        f'Day 11, part 2 solution: {max_x},{max_y},{max_size} (power '
        f'{max_power})')
