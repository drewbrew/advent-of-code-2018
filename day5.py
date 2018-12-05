#!/usr/bin/env python

import string

inputs = """<paste inputs here>"""


def react_polymer(polymer_string):
    """
    Iterate through polymer_string, replacing all instances where two
    adjacent characters are case-insensitive equal but not equal (i.e. A and a)
    with the empty string
    """
    iterations = 0
    original_string = polymer_string
    while True:
        original_string = polymer_string
        polymer_string = parse_polymer(polymer_string)
        iterations += 1
        if original_string == polymer_string:
            break
    return polymer_string


def parse_polymer(polymer_string):
    for index, char in enumerate(polymer_string):
        try:
            next = polymer_string[index + 1]
        except IndexError:
            # we've reached the end. Nothing can be done.
            return polymer_string
        if next.casefold() == char.casefold() and next != char:
            # strip these two chars
            polymer_string = polymer_string[:index] + polymer_string[
                index + 2:]
            # and return the result
            return polymer_string


def find_best_removal(polymer_string):
    results = {}
    for char in string.ascii_lowercase:
        if char.casefold() not in polymer_string.casefold():
            print('skipping', char)
            results[char] = len(polymer_string)
            continue
        shortened = polymer_string.replace(char, '')
        shortened = shortened.replace(char.upper(), '')
        results[char] = len(react_polymer(shortened))
        print(f'tested {char}; result {results[char]}')
    return sorted(results.items(), key=lambda k: k[1])[0]

if __name__ == '__main__':
    assert react_polymer('dabAcCaCBAcCcaDA') == react_polymer('dabCBAcaDA')
    assert find_best_removal('dabAcCaCBAcCcaDA') == ('c', 4), find_best_removal('dabAcCaCBAcCcaDA')
    fully_reacted = len(react_polymer(inputs))
    print('Day 5, part 1 solution:', fully_reacted)
    best_char, length = find_best_removal(inputs)
    print(f'Day 5, part 2 solution: remove {best_char} for length {length}')
