#!/usr/bin/env python
from collections import defaultdict

TEST_INPUT = r"""/->-\
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/""".split('\n')

PART_TWO_TEST_INPUT = r"""/>-<\
|   |
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/""".split('\n')

REAL_INPUT = r"""<paste inputs here>""".split('\n')


CART_CHARS = '^<>v'


class Cart:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
        self.dead = False
        self.turn_modulus = 0

    def __eq__(self, other):
        try:
            return self.position == other.position and self.direction == \
                other.direction and self.dead is other.dead
        except AttributeError:
            return False

    def __str__(self):
        return f'{self.position}, heading {self.direction}, dead? {self.dead}'


def parse_track(input_list):
    tracks = defaultdict(lambda: '')
    carts = []
    for y, line in enumerate(input_list):
        for x, char in enumerate(line):
            if char == '\n':
                raise ValueError('new line')
            if char in CART_CHARS:
                direction = {
                    '<': -1,
                    '>': 1,
                    '^': -1j,
                    'v': 1j
                }[char]
                carts.append(
                    Cart(
                        x + (y * 1j), direction,
                    )
                )
                part = {
                    '<': "-",
                    '>': '-',
                    '^': '|',
                    'v': '|',
                }[char]
            else:
                part = char
            if part in '\\/+':
                # it's a turn or intersection and therefore relevant
                tracks[(x + (y * 1j))] = part
    return tracks, carts


def turn_cart(cart, part):
    # game uses a downward-facing Y axis, which means we need to invert the
    # imaginary part of the cart's direction
    if not part:
        # we don't save going straight ahead
        return
    if part == '\\':
        # northeast/southwest corner
        if cart.direction.real == 0:
            # it's going up or down
            # e.g. if it's originally going down, new direction is
            # -1j * -1j = +1, so it's going right
            cart.direction *= -1j
        else:
            # it's going sideways
            cart.direction *= 1j
    elif part == '/':
        # NW/SE corner, same logic as above, only inverted operation
        if cart.direction.real == 0:
            cart.direction *= 1j
        else:
            cart.direction *= -1j
    elif part == '+':
        # need to turn it!
        # 1j ** 2 = -1
        # so if 0, new direction is -1j
        cart.direction *= -1j * (1j ** cart.turn_modulus)
        # then increment
        cart.turn_modulus = (cart.turn_modulus + 1) % 3

def part_one(input_list):
    tracks, carts = parse_track(input_list)
    while True:
        carts.sort(key=lambda c: (c.position.imag, c.position.real))
        for index, cart in enumerate(carts):
            cart.position += cart.direction
            if any(
                other.position == cart.position
                for other_index, other in enumerate(carts) if other != cart
            ):
                return cart.position
            part = tracks[cart.position]
            turn_cart(cart, part)


def part_two(input_list):
    tracks, carts = parse_track(input_list)
    while len(carts) > 1:
        carts.sort(key=lambda c: (c.position.imag, c.position.real))
        for index, cart in enumerate(carts):
            if cart.dead:
                continue
            cart.position += cart.direction
            for index2, other in enumerate(carts):
                if index != index2 and \
                        not other.dead and other.position == cart.position:
                    cart.dead = True
                    other.dead = True
                    break
            if cart.dead:
                continue
            part = tracks[cart.position]
            turn_cart(cart, part)
        carts = [i for i in carts if not i.dead]
    cart = carts[0]
    return carts[0].position


if __name__ == '__main__':
    print('testing inputs')
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 7 + 3j, part_one_result
    part_two_result = part_two(PART_TWO_TEST_INPUT)
    assert part_two_result == 6 + 4j, part_two_result
    print('tests passed')
    part_one_result = part_one(REAL_INPUT)
    part_two_result = part_two(REAL_INPUT)
    print(
        f'Day 13, part 1: {int(part_one_result.real)},'
        f'{int(part_one_result.imag)}')
    print(
        f'Day 13, part 2: {int(part_two_result.real)},'
        f'{int(part_two_result.imag)}')
