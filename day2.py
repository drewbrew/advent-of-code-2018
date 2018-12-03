#!/usr/bin/env python
from collections import Counter
import sys


def chars_different(box1, box2):
    """Count the number of characters that differ between box1 and box2"""
    diff = sum(
        1 if i != j else 0 for i, j in zip(box1, box2)
    )
    return diff


def common_chars(box1, box2):
    """Return all common characters between box1 and box2 in order

    >>> common_chars('abcdef', 'abddeg')
    'abde'
    """
    return ''.join(i if i == j else '' for i, j in zip(box1, box2))


raw = """<paste inputs here>""".split('\n')
counts = [Counter(i) for i in raw]


if __name__ == '__main__':
    threes = 0
    twos = 0

    for i in counts:
        if any(val == 3 for val in i.values()):
            threes += 1
        if any(val == 2 for val in i.values()):
            twos += 1

    print('Day 2, part 1 solution:', threes * twos)

    for box1 in raw:
        for box2 in raw:
            if chars_different(box1, box2) == 1:
                print('Day 2, part 2 solution:', common_chars(box1, box2))
                sys.exit(0)
