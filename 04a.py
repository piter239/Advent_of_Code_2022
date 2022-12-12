# solution to https://adventofcode.com/2022/day/4

def fully_contain(x1,y1,x2,y2):
    return (x1 - x2) * (y1 - y2) <= 0

def myinput():
    with open('04input.txt','r') as f:
        for line in f:
            yield line

import re

print(sum(fully_contain(*map(int, re.sub('[-,]', ' ', c).split())) for c in myinput()))

