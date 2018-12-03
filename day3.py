#!/usr/bin/env python

raw = """<paste inputs here>"""


def process_claim(claim):
    """Convert a claim row into a set of points"""
    claim_number, details = [i.strip() for i in claim.split('@')]
    # strip the leading #
    claim_number = int(claim_number[1:])
    coordinates, area = [i.strip() for i in details.split(':')]
    column, row = [int(i) for i in coordinates.split(',')]
    width, height = [int(i) for i in area.split('x')]
    claims = set(
        (x, y)
        for x in range(row, row + height)
        for y in range(column, column + width)
    )
    return claim_number, claims


def invert_claims(claims):
    """Convert a dict of {claim_number: claims} to {(x, y): {claim_numbers}}"""
    coordinates_claimed = {}
    for claim_number, coordinate_set in claims.items():
        for coordinates in coordinate_set:
            try:
                coordinates_claimed[coordinates].append(claim_number)
            except KeyError:
                coordinates_claimed[coordinates] = [claim_number]
    return coordinates_claimed


def find_uncontested_claim(claims, coordinates_claimed):
    """Find the single claim that is uncontested"""
    # first, eliminate all shared claims
    unshared_claims = set(
        key for key, val in coordinates_claimed.items() if len(val) == 1)
    # then we can use simple set theory:
    # if a claim's coordinates are a direct subset of the set of unshared
    # coordinates, its territory is solely its own
    isolated = [
        claim_number
        for claim_number, coordinate_set in claims.items()
        if coordinate_set.issubset(unshared_claims)
    ]
    assert len(isolated) == 1
    return isolated[0]


if __name__ == '__main__':
    claims = dict(process_claim(row) for row in raw.split('\n') if row)
    claimed = invert_claims(claims)
    shared = len(list(key for key, val in claimed.items() if len(val) > 1))
    print('Day 3, part 1 solution:', shared)
    uncontested = find_uncontested_claim(claims, claimed)
    print('Day 3, part 2 solution:', uncontested)
