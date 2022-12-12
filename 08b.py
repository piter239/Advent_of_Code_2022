# solution to https://adventofcode.com/2022/day/8

def myinput():
    with open('08input.txt', 'r') as f:
        for nextline in f:
            yield nextline

trees = [[int(c) for c in line.strip()] for line in myinput()]


q_size = len(trees)

if any(q_size != len(trees[i]) for i in range(q_size)):
    print("Not a quadrat this programm expects!")
    quit(1)


# field[i][j] is the scenic score
field = [[0] * q_size] + [[0] + [1] * (q_size-2) + [0] for i in range(1, q_size-1)] + [[0] * q_size]


#print(*field, sep='\n')

def max_score(field):
    return max([max(v) for v in field])

print(max_score(field))



def look_from_N(field, trees):
    ''' process the trees array, calculating the scenic score looking downfrom each inner point in array  field,
        multiplying the result with value already in array
    '''
    for i in range(1, q_size - 1):
        for j in range(1, q_size - 2):
            v_dist = 1
            while i + v_dist < q_size and trees[i + v_dist][j] < trees[i][j]:
                v_dist += 1
            if i + v_dist == q_size:
                v_dist -= 1
            field[i][j] *= v_dist


look_from_N(field, trees)
print(max_score(field))
print(*field, sep='\n')

trees = trees[::-1] # now N is actually S
field = field[::-1]

look_from_N(field, trees)
print(max_score(field))

t_trees = [list(row) for row in zip(*trees)]
t_field = [list(row) for row in zip(*field)]

look_from_N(t_field, t_trees)
print(max_score(t_field))

t_trees = t_trees[::-1]
t_field = t_field[::-1]

look_from_N(t_field, t_trees)
print(max_score(t_field))
print(*t_field, sep='\n')
