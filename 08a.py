# solution to https://adventofcode.com/2022/day/8

from collections import defaultdict

q_size = 99


def myinput():
    with open('08input.txt', 'r') as f:
        for nextline in f:
            yield nextline

# field[i][j] == 1 <=> tree i,j is visible from a direction in NEWS
field = [[0] * q_size for _ in range(q_size)]

def visible(field):
    return sum([sum(v) for v in field])



trees = [line.strip() for line in myinput()]

# now we look from N, S, W, E
# starting from N

def look_from_N(field, trees):
    ''' process the trees array, setting the visibility from N in array  field
    '''
    max_j = [-1] * q_size

    for i in range(q_size):
        for j in range(q_size):
            if int(trees[i][j]) > max_j[j]:
                field[i][j] = 1 # this tree can be seen
                max_j[j] = int(trees[i][j])


look_from_N(field, trees)
print(visible(field))

trees = trees[::-1] # now N is actually S
field = field[::-1]

look_from_N(field, trees)
print(visible(field))

t_trees = [''.join(row) for row in zip(*trees)]
t_field = [list(row) for row in zip(*field)]

look_from_N(t_field, t_trees)
print(visible(t_field))

t_trees = t_trees[::-1]
t_field = t_field[::-1]

look_from_N(t_field, t_trees)
print(visible(t_field))
