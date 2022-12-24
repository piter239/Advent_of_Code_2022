from copy import deepcopy

room = '''#E######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#'''.splitlines()


def read_input(filename):
    with open(filename) as f:
        source = f.read()
    lines = source.splitlines()
    return lines


dirs = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1), 'w': (0, 0)}


def find_start_goal(room):
    start = goal = None
    i = 0
    for j, c in enumerate(room[0]):
        if c == 'E':
            start = (i, j)
    i = len(room) - 1
    for j, c in enumerate(room[i]):
        if c == '.':
            goal = (i, j)
    return start, goal


class Grove:
    def __init__(self, room):
        self.room = [list(line) for line in room]
        self.start, self.goal = find_start_goal(room)
        self.elves = {self.start}
        self.width = len(room[0])
        self.height = len(room)
        self.torus = {'^': (self.height - 3, 0), 'v': (-(self.height - 3), 0), '<': (0, self.width - 3),
                      '>': (0, -(self.width - 3))}
        self.blizzards = set()
        self.blizzards_pos = set()
        self.get_blizzards(room)
        self.steps = 0

    def __str__(self):
        res = deepcopy(self.room)
        for c, i, j in self.blizzards:
            res[i][j] = c
        for i, j in self.elves:
            res[i][j] = 'E'
        return '\n'.join(''.join(line) for line in res)

    def get_blizzards(self, room):
        for i, line in enumerate(room):
            for j, c in enumerate(line):
                if c in '<>^v':
                    self.blizzards.add((c, i, j))
                    self.blizzards_pos.add((i, j))
                    self.room[i][j] = '.'

    def move_all_blizzards(self):
        new_blizzards = set()
        new_blizzards_pos = set()
        for c, i, j in self.blizzards:
            di, dj = dirs[c]
            if self.room[i + di][j + dj] == '#':
                di, dj = self.torus[c]
            new_blizzards.add((c, i + di, j + dj))
            new_blizzards_pos.add((i + di, j + dj))
        self.blizzards = new_blizzards
        self.blizzards_pos = new_blizzards_pos

    def move_elves(self):
        ''' move all elves to their all possible new positions a once after blizzards have moved'''
        new_elves = set()
        for curr in self.elves:
            i, j = curr
            for di, dj in dirs.values():
                if self.room[(i + di) % self.height][j + dj] != '#':
                    if (i + di, j + dj) not in self.blizzards_pos:
                        new_elves.add((i + di, j + dj))
        return new_elves

    def search4path(self):
        '''search for path from start to goal'''
        while True:
            print(f'step {self.steps}', self, sep='\n')
            self.move_all_blizzards()
            self.elves = self.move_elves()
            self.steps += 1
            if self.goal in self.elves:
                return self.steps

    def from_here_to_there_back_and_there_again(self):

        self.search4path()

        self.start, self.goal = self.goal, self.start
        self.elves = {self.start}

        self.search4path()

        self.start, self.goal = self.goal, self.start
        self.elves = {self.start}

        return self.search4path()


if __name__ == '__main__':
    room = read_input('24input.txt')
    grove = Grove(room)
    # part 1
    # print(grove.search4path())
    # part 2
    print(grove.from_here_to_there_back_and_there_again())
