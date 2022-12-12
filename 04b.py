# solution to https://adventofcode.com/2022/day/4#part2

def fully_contain(x1,y1,x2,y2):
    return (x1 - x2) * (y1 - y2) <= 0

def overlap(x1,y1,x2,y2):
    return x1 <= x2 <= y1 or x2 <= x1 <= y2

def myinput():
    with open('04input.txt','r') as f:
        for line in f:
            yield line

import re

print(sum(overlap(*map(int, re.sub('[-,]', ' ', c).split())) for c in myinput()))

