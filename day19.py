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

REAL_INPUT = """#ip 3
addi 3 16 3
seti 1 5 1
seti 1 4 4
mulr 1 4 5
eqrr 5 2 5
addr 5 3 3
addi 3 1 3
addr 1 0 0
addi 4 1 4
gtrr 4 2 5
addr 3 5 3
seti 2 6 3
addi 1 1 1
gtrr 1 2 5
addr 5 3 3
seti 1 1 3
mulr 3 3 3
addi 2 2 2
mulr 2 2 2
mulr 3 2 2
muli 2 11 2
addi 5 3 5
mulr 5 3 5
addi 5 3 5
addr 2 5 2
addr 3 0 3
seti 0 6 3
setr 3 8 5
mulr 5 3 5
addr 3 5 5
mulr 3 5 5
muli 5 14 5
mulr 5 3 5
addr 2 5 2
seti 0 2 0
seti 0 2 3""".split('\n')


def run_prog(puzzle_input, reg_0=0):
    registers = [reg_0, 0, 0, 0, 0, 0]
    instruction_ptr = int(puzzle_input[0].split()[-1])
    puzzle = puzzle_input[1:]
    while registers[instruction_ptr] < len(puzzle) and \
            registers[instruction_ptr] >= 0:
        line = puzzle[registers[instruction_ptr]]
        if not registers[instruction_ptr] % 100:
            print(line, registers)
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
    assert run_prog(TEST_INPUT) == [6, 5, 6, 0, 0, 9]
    print(run_prog(REAL_INPUT))
    print(run_prog(REAL_INPUT, 1))
