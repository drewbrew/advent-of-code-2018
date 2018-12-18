#!/usr/bin/env python

from dataclasses import dataclass
from typing import List

TEST_INPUT = """Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]""".split('\n')


REAL_INPUT = """<paste part 1 input here>""".split('\n')


REAL_PROG = """<paste part two input here>""".split('\n')


@dataclass
class OpcodeInfo:
    before: List
    opcodes: List
    result: List


def parse_input(input_lines):
    before = []
    opcodes = []
    after = []
    parsed = []
    for line in input_lines:
        if not line:
            continue
        if line.startswith('Before:'):
            before = [int(i) for i in line[9:-1].split(', ')]
        elif line.startswith('After'):
            after = [int(i) for i in line[9:-1].split(', ')]
        else:
            opcodes = [int(i) for i in line.split()]
        if before and after and opcodes:
            parsed.append(OpcodeInfo(before, opcodes, after))
            before = []
            after = []
            opcodes = []
    return parsed


def addr(registers, opcodes):
    """addr (add register) stores into register C the
    result of adding register A and register B."""
    test_result = registers[opcodes[1]] + registers[opcodes[2]]
    return test_result


def addi(registers, opcodes):
    """addi (add immediate) stores into register C the
    result of adding register A and value B."""
    test_result = registers[opcodes[1]] + opcodes[2]
    return test_result


def mulr(registers, opcodes):
    """mulr (multiply register) stores into register C
    the result of multiplying register A and register B."""
    test_result = registers[opcodes[1]] * registers[opcodes[2]]
    return test_result


def muli(registers, opcodes):
    """muli (multiply immediate) stores into register C the
    result of multiplying register A and value B."""
    test_result = registers[opcodes[1]] * opcodes[2]
    return test_result


def banr(registers, opcodes):
    """banr (bitwise AND register) stores into register C the
    result of the bitwise AND of register A and register B."""
    test_result = registers[opcodes[1]] & registers[opcodes[2]]
    return test_result


def bani(registers, opcodes):
    """bani (bitwise AND immediate) stores into register C the result of the
    bitwise AND of register A and value B."""
    test_result = registers[opcodes[1]] & opcodes[2]
    return test_result


def borr(registers, opcodes):
    """borr (bitwise OR register) stores into register C the result of the
    bitwise OR of register A and register B."""
    test_result = registers[opcodes[1]] | registers[opcodes[2]]
    return test_result


def bori(registers, opcodes):
    """bori (bitwise OR immediate) stores into register C the
    result of the bitwise OR of register A and value B."""
    test_result = registers[opcodes[1]] | opcodes[2]
    return test_result


def setr(registers, opcodes):
    """setr (set register) copies the contents of register A into register C.
    (Input B is ignored.)"""
    return registers[opcodes[1]]


def seti(registers, opcodes):
    """seti (set immediate) stores value A into register C.
    (Input B is ignored.)
    """
    return opcodes[1]


def gtir(registers, opcodes):
    """gtir (greater-than immediate/register) sets register C to 1
    if value A is greater than register B. Otherwise, register C is set to 0"""
    test_result = int(opcodes[1] > registers[opcodes[2]])
    return test_result


def gtii(registers, opcodes):
    """gtri (greater-than register/immediate) sets register C to 1 if
    register A is greater than value B. Otherwise, register C is set to 0."""
    test_result = int(registers[opcodes[1]] > opcodes[2])
    return test_result


def gtrr(registers, opcodes):
    """gtrr (greater-than register/register) sets register C to 1 if
    register A is greater than register B. Otherwise, register C is set to 0.
    """
    test_result = int(registers[opcodes[1]] > registers[opcodes[2]])
    return test_result


def eqir(registers, opcodes):
    """eqir (equal immediate/register) sets register C to 1 if value A is
    equal to register B. Otherwise, register C is set to 0."""
    test_result = int(opcodes[1] == registers[opcodes[2]])
    return test_result


def eqri(registers, opcodes):
    """eqri (equal register/immediate) sets register C to 1 if register A
    is equal to value B. Otherwise, register C is set to 0."""
    return int(registers[opcodes[1]] == opcodes[2])


def eqrr(registers, opcodes):
    """eqrr (equal register/register) sets register C to 1 if register A is
    equal to register B. Otherwise, register C is set to 0.
    """
    return int(registers[opcodes[1]] == registers[opcodes[2]])


def test_instruction_set(instruction_set):
    expected_result = instruction_set.result[instruction_set.opcodes[3]]
    funcs = [
        addi, addr, muli, mulr, bani, banr, bori, borr, seti, setr,
        gtii, gtir, gtrr, eqir, eqri, eqrr,
    ]
    like_opcodes = 0
    for func in funcs:
        if func(
            instruction_set.before, instruction_set.opcodes,
        ) == expected_result:
            like_opcodes += 1
    return like_opcodes


def get_opcode_map(part_one_input_list):
    possible_candidates = {}
    eliminated_candidates = {}
    funcs = [
        addi, addr, muli, mulr, bani, banr, bori, borr, seti, setr,
        gtii, gtir, gtrr, eqir, eqri, eqrr,
    ]
    for instruction_set in part_one_input_list:
        opcode = instruction_set.opcodes[0]
        expected_result = instruction_set.result[instruction_set.opcodes[3]]
        for func in funcs:
            if func in eliminated_candidates.get(opcode, set()):
                continue
            if func(
                instruction_set.before, instruction_set.opcodes,
            ) != expected_result:
                try:
                    eliminated_candidates[opcode].add(func)
                except KeyError:
                    eliminated_candidates[opcode] = {func}
                try:
                    possible_candidates[opcode].remove(func)
                except KeyError:
                    # don't care
                    pass
            else:
                try:
                    possible_candidates[opcode].add(func)
                except KeyError:
                    possible_candidates[opcode] = {func}
    definite_map = {}
    iterations = 0
    while True:
        for opcode, candidates in list(
                possible_candidates.items()):
            if opcode in definite_map:
                del possible_candidates[opcode]
            if len(candidates) == 1:
                known = list(candidates)[0]
                definite_map[opcode] = known
                for other_opcode, other_candidates in list(
                        possible_candidates.items()):
                    if other_opcode != opcode:
                        try:
                            other_candidates.remove(known)
                        except KeyError:
                            # don't care
                            pass
                        if not other_candidates:
                            del possible_candidates[other_opcode]
        if not possible_candidates:
            break
        iterations += 1
        if iterations > 100:
            print('oh noes', '\n'.join(
                f'{opcode}: {list(i.__name__ for i in func_list)}'
                for opcode, func_list in possible_candidates.items()
            ), '---', '\n'.join(
                f'{opcode}: {func.__name__}'
                for opcode, func in sorted(definite_map.items())
            ))
            raise RuntimeError()
    print('Opcode map:')
    print(
        '\n'.join(
            f'{opcode}: {func.__name__}'
            for opcode, func in sorted(definite_map.items())
        ),
    )
    assert len(definite_map) == 16
    return definite_map


def part_two(instruction_list, opcode_map):
    registers = [0, 0, 0, 0]
    for instruction in instruction_list:
        target_register = instruction[3]
        try:
            func = opcode_map[instruction[0]]
        except KeyError:
            print(
                f'No way to handle {instruction}'
            )
            raise
        result = func(registers, instruction)
        registers[target_register] = result
    return registers


if __name__ == '__main__':
    test_input = parse_input(TEST_INPUT)
    assert len(test_input) == 1
    test_result = test_instruction_set(test_input[0])
    assert test_result == 3, test_result
    parsed_input = parse_input(REAL_INPUT)
    like_three_or_more = 0
    for instruction_set in parsed_input:
        like_opcodes = test_instruction_set(instruction_set)
        if like_opcodes >= 3:
            like_three_or_more += 1
    print('Day 17, part 1 solution', like_three_or_more)
    opcode_map = get_opcode_map(parsed_input)
    program = [[int(i) for i in line.split()] for line in REAL_PROG]
    print('Day 17, part 2 solution', part_two(program, opcode_map)[0])
