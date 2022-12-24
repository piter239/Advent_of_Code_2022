# Your task is to implement a function that simulates the movement of the Elves in the grove.
# The function should take in the following parameters:
#
# A list of strings representing the initial positions of the Elves in the grove.
# Each string represents a row in the grove, and the characters '.' and '#' represent empty ground and Elves, respectively.
#
# An integer representing the number of rounds to simulate.
# The Elves follow a time-consuming process to figure out where they should each go.
# The process consists of some number of rounds during which Elves alternate between considering where to move and actually moving.
#
# During the first half of each round, each Elf considers the eight positions adjacent to themselves.
# If no other Elves are in one of those eight positions, the Elf does not do anything during this round.
# Otherwise, the Elf looks in each of four directions in the following order and proposes moving one step in the first valid direction:
#
# If there is no Elf in the N, NE, or NW adjacent positions, the Elf proposes moving north one step.
# If there is no Elf in the S, SE, or SW adjacent positions, the Elf proposes moving south one step.
# If there is no Elf in the W, NW, or SW adjacent positions, the Elf proposes moving west one step.
# If there is no Elf in the E, NE, or SE adjacent positions, the Elf proposes moving east one step.
# After each Elf has had a chance to propose a move, the second half of the round can begin.
# Simultaneously, each Elf moves to their proposed destination tile if they were the only Elf to propose moving to that position.
# If two or more Elves propose moving to the same position, none of those Elves move.
#
# Finally, at the end of the round, the first direction the Elves considered is moved to the end of the list of directions.
# For example, during the second round, the Elves would try proposing a move to the south first, then west, then east, then north.
# On the third round, the Elves would first consider west, then east, then north, then south.
#
# The function should return a list of strings representing the final positions of the Elves in the grove after the specified number of rounds.
#
# Example:
#
# Input:

grove = [
    "....#..",
    "..###.#",
    "#...#.#",
    ".#...##",
    "#.###..",
    "##.#.##",
    ".#..#.."
]

# simplest test to check that move_elves() works
# grove = [".....",
#          "..##.",
#          "..#..",
#          ".....",
#          "..##.",
#          "....."]

from collections import defaultdict
from copy import deepcopy

def empty_fn(): return '.'


def create_map(grove):
    map_dict = defaultdict(empty_fn)  # default value is empty space
    for i, line in enumerate(grove):
        for j, char in enumerate(line):
            map_dict[(i, j)] = char
            if char == '#':
                for dir in dirs:
                    if sum(map_dict[i + x, j + y] == '#' for x, y in dir_check[dir]) == 3:
                        pass    # we are locking at surrounding cells to be sure they are initialized
    return map_dict


dirs = ['N', 'S', 'W', 'E']
dir_moves = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
neighbours = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
dir_check = {'N': [(-1, 0), (-1, -1), (-1, 1)],
             'S': [(1, 0), (1, -1), (1, 1)],
             'W': [(0, -1), (-1, -1), (1, -1)],
             'E': [(0, 1), (-1, 1), (1, 1)]}


def move_elves(grove, rounds=0):
    if not rounds:   # part 2
        rounds = 1000000000
    map_dict = create_map(grove)
    for i in range(rounds):
        print(f"== Round {i + 1} ==")   # round 1 is the first round
        #print_map(map_dict)
        moved = False
        suggested_moves = defaultdict(list)  # key is position WHERE to move, value is list of suggested moves from WHERE to move
        for pos, char in map_dict.items():
            if char == '#':
                if all(map_dict[pos[0] + x, pos[1] + y] == '.' for x, y in neighbours):
                    continue
                moved = True
                for dir in dirs:
                    if not any(map_dict[pos[0] + x, pos[1] + y] == '#' for x, y in dir_check[dir]):
                        suggested_moves[pos[0] + dir_moves[dir][0], pos[1] + dir_moves[dir][1]] += [pos]
                        break
        for to_pos, from_pos in suggested_moves.items():
            if len(from_pos) == 1:
                map_dict[to_pos] = '#'
                map_dict[from_pos[0]] = '.'
                for dir in dirs:
                    if sum(map_dict[to_pos[0] + x, to_pos[1] + y] == '#' for x, y in dir_check[dir]) == 3:
                        pass    # we are locking at surrounding cells to be sure they are initialized
        dirs.append(dirs.pop(0))  # move first direction to the end of the list
        print("Round finished", i + 1, end=' ')
        if not moved:
            print("No elves moved!!!")
            break
        count_empty(map_dict)
    return map_dict


def print_map(map_dict):
    max_x = max(map_dict.keys(), key=lambda x: x[0])[0]
    max_y = max(map_dict.keys(), key=lambda x: x[1])[1]
    min_x = min(map_dict.keys(), key=lambda x: x[0])[0]
    min_y = min(map_dict.keys(), key=lambda x: x[1])[1]
    for i in range(min_x, max_x + 1):
        for j in range(min_y, max_y + 1):
            print(map_dict[i, j], end='')
        print()


def count_empty(map_dict):
    '''find the smallest rectangle that contains all elves
    and count the number of empty spaces inside'''
    min_x = min_y = 1000
    max_x = max_y = 0
    for pos in map_dict.keys():
        if map_dict[pos] == '#':
            min_x = min(min_x, pos[0])
            max_x = max(max_x, pos[0])
            min_y = min(min_y, pos[1])
            max_y = max(max_y, pos[1])
    number_of_empty = 0
    number_of_elves = 0
    for i in range(min_x, max_x + 1):
        for j in range(min_y, max_y + 1):
            if map_dict[i, j] == '.':
                number_of_empty += 1
            elif map_dict[i, j] == '#':
                number_of_elves += 1
            else:
                print(f"ERROR: {map_dict[i, j]}")
                quit()
    print(f"{number_of_empty} empty and {number_of_elves} elves")
    return number_of_empty


def test_part1(grove):
    state = move_elves(grove, 10)
    #print_map(state)
    print(count_empty(state))
    assert count_empty(state) == 110

    with open('23input.txt') as f:
        grove = f.read().splitlines()
    state0 = create_map(grove)
    #print_map(state0)
    count_empty(state0)

    state = move_elves(grove, 10)
    #print_map(state)
    print(count_empty(state))

def test_part2(grove):
    with open('23input.txt') as f:
        grove = f.read().splitlines()
    state = move_elves(grove)



if __name__ == '__main__':
    test_part1(grove)
    test_part2(grove)
