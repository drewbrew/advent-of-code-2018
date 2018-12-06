#!/usr/bin/env python

inputs = """<paste inputs here>"""

lines = inputs.split('\n')
source = []
for line in lines:
    i, j = line.split(', ')
    source.append((int(i), int(j)))

part_2_threshold = 10000


def get_outer_grid(coordinate_list):
    """Get the boundaries of the outer grid for ease of plotting"""
    x_coordinates = list(sorted(i[0] for i in coordinate_list))
    y_coordinates = list(sorted(i[1] for i in coordinate_list))
    min_x = x_coordinates[0] - 2
    max_x = x_coordinates[-1] + 2
    min_y = y_coordinates[0] - 2
    max_y = y_coordinates[-1] + 2
    return ((min_x, min_y), (max_x, max_y))


def closest_input_to_point(x, y, coordinate_list, outer_grid):
    """Return the point closest to x, y by manhattan distance

    Returns -1 for tie
    """
    best_index = -1
    min_coords, max_coords = outer_grid
    best_dist = max_coords[0] - min_coords[0] + max_coords[1] - min_coords[0]
    for index, (x_comp, y_comp) in enumerate(coordinate_list):
        dist = abs(x_comp - x) + abs(y_comp - y)
        if dist < best_dist:
            best_index = index
            best_dist = dist
        elif dist == best_dist:
            # mark as a tie
            best_index = -1
    return (best_index, best_dist)


def distance_to_coordinate(x, y, coord_x, coord_y):
    return abs(x - coord_x) + abs(y - coord_y)


def infinite_areas(closest_input_dict, outer_grid):
    """Return a set of indexes which extend infintely"""
    (min_x, min_y), (max_x, max_y) = outer_grid
    result = set()
    for input_index, coordinate_list in closest_input_dict.items():
        if input_index == -1:
            continue
        x_coords = set(i[0] for i in coordinate_list)
        y_coords = set(i[1] for i in coordinate_list)
        if x_coords.intersection({min_x, max_x}) or y_coords.intersection(
                {min_y, max_y}):
            # it's on the perimeter
            result.add(input_index)
    return result


if __name__ == '__main__':
    test_input = [(1, 1), (1, 6), (8, 3), (3, 4), (5, 5), (8, 9)]
    test_outer_grid = get_outer_grid(test_input)
    assert test_outer_grid == ((-1, -1), (10, 11))
    outer_grid = get_outer_grid(source)
    print('outer grid is', outer_grid)
    closest_points = {index: [] for index in range(-1, len(source))}
    assert closest_input_to_point(5, 0, test_input, test_outer_grid)[0] == -1
    (min_x, min_y), (max_x, max_y) = outer_grid
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            closest_input, distance = closest_input_to_point(x, y, source, outer_grid)
            closest_points[closest_input].append((x, y))
    # ok, now we have our grid
    infinites = infinite_areas(closest_points, outer_grid)
    largest_finite = max(
        len(v) for k, v in closest_points.items() if k not in infinites and k != -1)
    print('day 6, part 1 solution:', largest_finite)
    safe_spots = 0
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            distance_to_coordinates = sum(
                distance_to_coordinate(x, y, coord_x, coord_y)
                for coord_x, coord_y in source
            )
            if distance_to_coordinates < part_2_threshold:
                # we have a safe spot
                safe_spots += 1
    print('day 6, part 2 solution:', safe_spots)
