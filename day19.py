#!/usr/bin/env python

import day16

TEST_INPUT = """#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5""".split('\n')

REAL_INPUT = """<paste inputs here>""".split('\n')


def run_prog(puzzle_input, reg_0=0, go_through_all=False):
    registers = [reg_0, 0, 0, 0, 0, 0]
    instruction_ptr = int(puzzle_input[0].split()[-1])
    puzzle = puzzle_input[1:]
    while 0 <= registers[instruction_ptr] < len(puzzle):
        if not go_through_all and registers[instruction_ptr] == 1:
            # once we hit this point, the code basically adds up all the
            # factors of register 2 and store them in register 0.
            # Note your puzzle input will probably use a different register
            # than mine, so try all registers 1-5 EXCEPT your instruction
            # pointer
            return sum(
                i for i in range(1, registers[2] + 1)
                if registers[2] % i == 0
            )
        line = puzzle[registers[instruction_ptr]]
        func_name, operand_1, operand_2, result_reg = line.split()
        operand_1 = int(operand_1)
        operand_2 = int(operand_2)
        result_reg = int(result_reg)
        func = getattr(day16, func_name)
        registers[result_reg] = func(registers, [0, operand_1, operand_2])
        registers[instruction_ptr] += 1
    registers[instruction_ptr] -= 1
    return registers


if __name__ == '__main__':
    assert run_prog(TEST_INPUT, go_through_all=True) == [6, 5, 6, 0, 0, 9]
    print(run_prog(REAL_INPUT))
    print(run_prog(REAL_INPUT, 1))
