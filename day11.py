#!/usr/bin/env python

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


def power_level(x, y, serial_number):
    """Find the fuel cell's rack ID, which is its X coordinate plus 10.
    Begin with a power level of the rack ID times the Y coordinate.
    Increase the power level by the value of the grid serial number
        (your puzzle input).
    Set the power level to itself multiplied by the rack ID.
    Keep only the hundreds digit of the power level
        (so 12345 becomes 3; numbers with no hundreds digit become 0).
    Subtract 5 from the power level."""
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
    grid = {}
    for y in range(1, max_y + 1):
        for x in range(1, max_x + 1):
            grid[(x, y)] = power_level(x, y, serial_number) if x and y else 0
    return grid


def max_power_area(grid, size=3):
    areas = {}
    max_coords = max(grid)
    for x in range(max_coords[0]):
        for y in range(max_coords[1]):
            if x == 0:
                continue
            if y == 0:
                continue
            area_power = sum(
                grid.get((test_x, test_y), 0)
                for test_x in range(x, x + size)
                for test_y in range(y, y + size)
            )
            areas[(x, y)] = area_power
    coords, power = list(
        sorted(areas.items(), key=lambda k: k[1], reverse=True))[0]
    return coords, power


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
