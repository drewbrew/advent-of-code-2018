#!/usr/bin/env python

import string

inputs = """<paste inputs here>"""


def react_polymer(polymer_string):
    """
    Iterate through polymer_string, replacing all instances where two
    adjacent characters are case-insensitive equal but not equal (i.e. A and a)
    with the empty string
    """
    # convert to a list since strings are immutable
    polymer_list = [i for i in polymer_string]
    index = 0
    while index < len(polymer_string) - 1:
        char = polymer_list[index]
        try:
            next_char = polymer_list[index + 1]
        except IndexError:
            break
        if next_char.casefold() == char.casefold() and next_char != char:
            # remove the char at index twice to get rid of char and next_char
            char1 = polymer_list.pop(index)
            char2 = polymer_list.pop(index)
            assert char1 == char
            assert char2 == next_char
            index = max([index - 2, 0])
            continue
        index += 1
    # Not technically necessary, but I like to maintain type coherence
    polymer_string = ''.join(polymer_list)
    return polymer_string


def find_best_removal(polymer_string):
    best_char = ''
    best_result = len(polymer_string)
    for char in string.ascii_lowercase:
        if char.casefold() not in polymer_string.casefold():
            print('skipping', char)
            continue
        shortened = polymer_string.replace(char, '')
        shortened = shortened.replace(char.upper(), '')
        result = len(react_polymer(shortened))
        print(f'tested {char}; result {result}')
        if result < best_result:
            best_char = char
            best_result = result
    return best_char, best_result


if __name__ == '__main__':
    assert react_polymer('dabAcCaCBAcCcaDA') == react_polymer('dabCBAcaDA')
    assert find_best_removal('dabAcCaCBAcCcaDA') == (
        'c', 4,
    ), find_best_removal('dabAcCaCBAcCcaDA')
    fully_reacted = len(react_polymer(inputs))
    print('Day 5, part 1 solution:', fully_reacted)
    best_char, length = find_best_removal(inputs)
    print(f'Day 5, part 2 solution: remove {best_char} for length {length}')
