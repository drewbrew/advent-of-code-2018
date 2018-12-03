#!/usr/bin/env python

raw = """<paste inputs here>""".split('\n')
source = [int(i) if i.startswith('-') else int(i[1:]) for i in raw]

print('Day 1, part 1 solution:', sum(source))

continuing = True
freqs_seen = {0}
running_total = 0
iterations = 0

while continuing:
    iterations += 1
    for i in source:
        running_total += i
        if running_total in freqs_seen:
            continuing = False
            print(
                'Day 1, part 2 solution', running_total,
                'on iteration', iterations,
            )
            break
        freqs_seen.add(running_total)
