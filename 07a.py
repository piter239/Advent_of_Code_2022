# solution to https://adventofcode.com/2022/day/7

from collections import defaultdict


def myinput():
    with open('07input.txt', 'r') as f:
        for nextline in f:
            yield nextline



file = myinput()

dir_size = defaultdict(int)
sub_dirs = defaultdict(list)

def full_name(path, name=''):
    return '/'.join(path + [name])

curr_path = []
for line in file:
    h, *t = line.split()
    if h == '$':    # $ command [arg]
        com, *arg = t
        if com == 'cd':
            dir = arg[0]
            if dir == '..':
                completed_dir = full_name(curr_path)
                curr_path.pop()
                dir_size[full_name(curr_path)] += dir_size[completed_dir]
            elif dir == '/':
                curr_path = ['']
            else:
                curr_path.append(dir)
        elif com == 'ls':
            pass
    elif h == 'dir':    # dir name
        sub_dirs[full_name(curr_path)] += [t[0]]
    else:   # file_size file_name[.ext]
        dir_size[full_name(curr_path)] += int(h)

print(*dir_size.items(), sep='\n')
print(*sub_dirs.items(), sep='\n')

print(sum(c for c in dir_size.values() if c <= 100000))
