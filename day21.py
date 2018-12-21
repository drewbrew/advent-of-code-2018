#!/usr/bin/env python

# NOTE: There is only one value that matters from the real input here.
# There's a seti <big number> <irrelevant> <register number, mine was 3>
# instruction around step 7. That big number goes in the LARGEST_SETI_VALUE

LARGEST_SETI_VALUE = 14070682


def run_prog(reg0):
    seen = set()
    reg_3_seen = set()
    # replace 14070682 with the largest "seti" value in your instructions
    # 65536 is pre-seeded based on `bori 3 65536 2` at step 6
    # your register numbers will probably be different, but it's irrelevant
    # My instruction pointer is reg 5, so it's untouched here
    registers = [reg0, 0, 65536, LARGEST_SETI_VALUE, 0, 0]
    while True:
        # bani 2 255 1
        registers[1] = registers[2] % 256
        registers[3] += registers[1]
        # This is these three steps
        # (remember that &= (2**n - 1) is equivalent to %= 2**n)
        # bani 3 16777215 3
        # muli 3 65899 3
        # bani 3 16777215 3
        registers[3] = (registers[3] % (2 ** 24) * 65899) % (2 ** 24)
        # if reg 2 < 256, then we successfully escaped. reg 3 has the answer
        # we need
        if registers[2] < 256:
            if not reg_3_seen:
                # this is our first successful escape, which is what part 1
                # wants
                print('Part 1 solution', registers[3])
            if registers[3] not in reg_3_seen:
                final = registers[3]
            reg_3_seen.add(registers[3])
            registers[2] = registers[3] | (2 ** 16)
            if registers[2] in seen:
                print('Part 2 solution', final)
                break
            seen.add(registers[2])
            registers[3] = LARGEST_SETI_VALUE
            continue
        registers[2] = int(registers[2] / 256)


if __name__ == '__main__':
    run_prog(0)
