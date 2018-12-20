#!/usr/bin/env python
import networkx


TEST_INPUTS = {
    r'^WNE$': 3,
    r'^ENWWW(NEEE|SSE(EE|N))$': 10,
    r'^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$': 18,
    r'^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$': 23,
    r'^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$': 31,
}

REAL_INPUT = r'<paste inputs here>'



def max_distance(puzzle_input, part_two=False):
    maze = networkx.Graph()
    puzzle = puzzle_input[1:-1]
    # current positions we're building branches on
    positions = {0}
    group_stack = []
    starts, finishes = {0}, set()
    for char in puzzle:
        if char == '|':
            # branch point!
            finishes.update(positions)
            positions = starts
        elif char in 'NWSE':
            # moving! add the edges and update position
            # use the complex plane with E/W being real and N/S being imaginary
            direction = {
                'N': 1j, 'E': 1, 'S': -1j, 'W': -1
            }[char]
            maze.add_edges_from(
                (point, point + direction) for point in positions
            )
            positions = {point + direction for point in positions}
        elif char == '(':
            # start of group
            group_stack.append((starts, finishes))
            starts, finishes = positions, set()
        elif char == ')':
            # end of group
            positions.update(finishes)
            starts, finishes = group_stack.pop()
    # now let networkx do its thing
    lengths = networkx.algorithms.shortest_path_length(maze, 0)
    if part_two:
        return len(list(i for i in lengths.values() if i >= 1000))
    return max(lengths.values())



if __name__ == '__main__':
    for test_input, expected_result in TEST_INPUTS.items():
        test_distance = max_distance(test_input)
        assert test_distance == expected_result, (
            test_input, test_distance, expected_result)
    print('tests passed')
    print(max_distance(REAL_INPUT))
    print(max_distance(REAL_INPUT, True))
