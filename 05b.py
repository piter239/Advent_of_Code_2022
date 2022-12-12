# solution to https://adventofcode.com/2022/day/5

from collections import defaultdict


def myinput():
    with open('05input.txt', 'r') as f:
        for nextline in f:
            yield nextline


file = myinput()

stacks = defaultdict(list)

for line in file:
    if line == '\n':
        break

    for i in range(1, len(line), 4):
        if line[i] != ' ' and line[i].isalpha():
            stacks[(i-1) // 4 + 1] += [line[i]]

for k in stacks:
    stacks[k] = stacks[k][::-1]
print(*stacks.items(),sep='\n')

for line in file:
    d = line.split()
    count, stack_from, stack_to = map(int, (d[1], d[3], d[5]))

    stacks[stack_to] += stacks[stack_from][-count:]
    stacks[stack_from] = stacks[stack_from][:-count]

for i in sorted(stacks.keys()):
    print(end=stacks[i][-1])

