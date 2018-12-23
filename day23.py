#!/usr/bin/env python

TEST_INPUT = """pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1""".split('\n')

PART_TWO_TEST_INPUT = """pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5""".split('\n')

REAL_INPUT = """<paste inputs here>""".split('\n')


def parse_input(puzzle_input):
    bots = {}
    for line in puzzle_input:
        pos, rad = line.split('>, r=')
        rad = int(rad)
        x, y, z = [int(i) for i in pos[5:].split(',')]
        if not bots:
            print(line, x, y, z, rad)
        bots[x, y, z] = rad
    return bots


def bots_in_range(bots):
    in_range = {}
    # calc the number of bots within range of each bot
    for bot, radius in bots.items():
        x, y, z = bot
        in_range[bot] = sum(
            1 for x1, y1, z1 in bots
            if abs(x1 - x) + abs(y1 - y) + abs(
                z1 - z
            ) <= radius
        )
    return in_range


def part_one(puzzle_input):
    bots = parse_input(puzzle_input)
    in_range = bots_in_range(bots)
    max_signal_range = list(sorted(
        bots.items(), key=lambda k: k[1],
        reverse=True,
    ))[0][0]
    return in_range[max_signal_range]


def part_two(puzzle_input):
    bots = parse_input(puzzle_input)
    x_list = [x[0] for x in bots]
    y_list = [x[1] for x in bots]
    z_list = [x[2] for x in bots]

    dist = 1
    # do a bisecting-ish search, basically cutting the grid in half
    while dist < max(x_list) - min(x_list):
        dist *= 2

    while True:
        max_bots_in_range = 0
        best = None
        best_distance_from_origin = float('inf')
        for x in range(min(x_list), max(x_list) + 1, dist):
            for y in range(min(y_list), max(y_list) + 1, dist):
                for z in range(min(z_list), max(z_list) + 1, dist):
                    bots_in_range = 0
                    for (bx, by, bz), bot_radius in bots.items():
                        calc = abs(x - bx) + abs(y - by) + abs(z - bz)
                        if (calc - bot_radius) / dist <= 0:
                            # node is in "range"
                            # (scaled by the distance factor)
                            bots_in_range += 1
                    if bots_in_range > max_bots_in_range:
                        # we've reached a new max for this x/y coordinate
                        max_bots_in_range = bots_in_range
                        best_distance_from_origin = abs(x) + abs(y) + abs(z)
                        best = (x, y, z)
                    elif bots_in_range == max_bots_in_range:
                        # same max; is this one closer?
                        if abs(x) + abs(y) + abs(z) < \
                                best_distance_from_origin:
                            best_distance_from_origin = abs(x) + abs(y) + abs(
                                z)
                            best = (x, y, z)

        # now we're done with that "grid"
        # scale back down and focus in on the area we found our
        # best point in
        if dist == 1:
            # no more downscaling necessary
            # this is our winning manhattan distance
            return best_distance_from_origin
        else:
            # shrink the grid
            x_list = [best[0] - dist, best[0] + dist]
            y_list = [best[1] - dist, best[1] + dist]
            z_list = [best[2] - dist, best[2] + dist]
            dist = int(dist / 2)


if __name__ == '__main__':
    test_part_one = part_one(TEST_INPUT)
    assert test_part_one == 7, test_part_one
    test_part_two = part_two(PART_TWO_TEST_INPUT)
    assert test_part_two == sum([12, 12, 12]), test_part_two
    print('tests passed')
    print(part_one(REAL_INPUT))
    print(part_two(REAL_INPUT))
