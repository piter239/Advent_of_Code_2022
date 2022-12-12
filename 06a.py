# solution to https://adventofcode.com/2022/day/6
marker_length = 140


def myinput():
    with open('06input.txt', 'r') as f:
        for nextline in f:
            yield nextline

file = myinput()

line = file.__next__()

marker_length = 140

res = 0
length = 1

while length < marker_length and res+length < len(line):
    if line[res + length] in line[res: res + length]:
        res, length = res + 1, 1
    else:
        length += 1
if res+length < len(line):
    print(res + length)
    print(res, length, line[res:res + length])
else:
    print("EOL. No marker", marker_length, "chars long found")
