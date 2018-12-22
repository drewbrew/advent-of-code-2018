#!/usr/bin/env python
import heapq

TEST_DEPTH = 510
TEST_TARGET = (10, 10)

REAL_DEPTH = 7305
REAL_TARGET = (13, 734)


def geologic_index(x, y, target, depth, levels):
    """The region at 0,0 (the mouth of the cave) has a geologic index of 0.
    The region at the coordinates of the target has a geologic index of 0.
    If the region's Y coordinate is 0, the geologic index is its X coordinate
        times 16807.
    If the region's X coordinate is 0, the geologic index is its Y coordinate
        times 48271.
    Otherwise, the region's geologic index is the result of multiplying the
        erosion levels of the regions at X-1,Y and X,Y-1.
    """
    if (x, y) in {(0, 0), target}:
        return 0
    if not x:
        return y * 48271
    if not y:
        return x * 16807
    try:
        return levels[(x, y)]
    except KeyError:
        one_left = erosion_level(x - 1, y, target, depth, levels)
        one_up = erosion_level(
            x, y - 1, target, depth, levels)
        levels[(x, y)] = one_left * one_up
        return levels[(x, y)]


def erosion_level(x, y, target, depth, levels):
    return (geologic_index(x, y, target, depth, levels) + depth) % 20183


def risk(x, y, target, depth, levels):
    return erosion_level(x, y, target, depth, levels) % 3


def neighbors(x, y, tool, target, depth, levels):
    for new_x, new_y in (
            (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
        if 0 <= new_x and 0 <= new_y:
            r = risk(new_x, new_y, target, depth, levels)
            for new_tool in range(3):
                if r != new_tool and r != tool:
                    yield new_x, new_y, new_tool, 8 \
                        if tool != new_tool else 1


def navigate(target, depth, levels):
    queue = [(0, 0, 0, 1)]  # (minutes, x, y, cannot)
    distances = {
        (0, 0, 1): 0,
    }
    while queue:
        # heavily influenced by reddit spoilers thread
        minutes, x, y, tool = heapq.heappop(queue)
        if (x, y, tool) == target + (1, ):
            # we're at the target and we've equipped the right tool
            return minutes
        if x > 4 * target[0] or y > 3 * target[1]:
            # way out in left field
            continue
        if distances.get((x, y, tool), 0) < minutes:
            # we've already been here, so it doesn't make sense to
            # loop and waste time
            continue
        for new_x, new_y, new_tool, time in neighbors(
            x, y, tool, target, depth, levels
        ):
            if minutes + time < distances.get(
                (new_x, new_y, new_tool),
                float('inf'),
            ):
                # we found a faster path here
                distances[new_x, new_y, new_tool] = minutes + time
                heapq.heappush(
                    queue, (minutes + time, new_x, new_y, new_tool))


if __name__ == '__main__':
    test_levels = {}
    test_inputs = {
        (1, 0): 17317,
        (0, 1): 8415,
        (1, 1): 1805,
        (10, 10): 510,
    }
    for (x, y), result in test_inputs.items():
        test_result = erosion_level(x, y, TEST_TARGET, TEST_DEPTH, test_levels)
        assert test_result == result, (x, y, test_result, result)
    assert sum(
        erosion_level(x, y, TEST_TARGET, TEST_DEPTH, test_levels) % 3
        for x in range(11)
        for y in range(11)
    ) == 114
    test_part_two = navigate(TEST_TARGET, TEST_DEPTH, test_levels)
    assert test_part_two == 45, test_part_two
    print('tests passed')
    real_levels = {}
    print(sum(
        erosion_level(x, y, REAL_TARGET, REAL_DEPTH, real_levels) % 3
        for x in range(REAL_TARGET[0] + 1) for y in range(REAL_TARGET[1] + 1)))
    print(navigate(REAL_TARGET, REAL_DEPTH, real_levels))
