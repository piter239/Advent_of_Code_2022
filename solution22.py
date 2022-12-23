# Task: Implement a function that takes in a map of a board represented as a string and a string of instructions,
# and returns the final password.
#
# Instructions:
#
# Parse the input string to create a 2D array representation of the board.
# The board is a rectangle of open tiles (.) and solid walls (#).
# Initialize variables for the current row, column, and facing (0 for right, 1 for down, 2 for left, 3 for up).
# Set the current row and column to the leftmost open tile of the top row.
# Iterate through the instructions string. For each number, move the current position in the direction the player
# is facing by that number of tiles. If the player encounters a wall, stop moving forward and continue with the next instruction.
# For each letter, turn the player 90 degrees in the specified direction (clockwise for R, counterclockwise for L).
# If the current position is off the board, wrap around to the other side of the board. If the next tile after wrapping
# around is a wall, stop movement before actually wrapping.
#
# Calculate the final password as 1000 times the final row plus 4 times the final column plus the final facing.
# Return the final password.
# Example:
#
# input (spaces are significant):
#        ...#
#         .#..
#         #...
#         ....
# ...#.......#
# ........#...
# ..#....#....
# ..........#.
#         ...#....
#         .....#..
#         .#......
#         ......#.
#
# 10R5L5R10L4R5L5
# output: 6032

import re


def split_instructions(instructions_string):
    # Use a regular expression to match the pattern of alternating numbers and letters
    instructions = re.findall(r'\d+|[A-Z]', instructions_string)
    return instructions


# Test the function
def test_split_instructions():
    assert split_instructions('10R5L5R10L4R5L5') == ['10', 'R', '5', 'L', '5', 'R', '10', 'L', '4', 'R', '5', 'L', '5']


def read_map(input_source):
    map_dict = {}

    for row, line in enumerate(input_source):
        if line == '':
            break  # Stop reading the map when the first blank line is encountered - the rest of the file is instructions
        for col, c in enumerate(line):
            if c in [".", "#"]:
                map_dict[(row, col)] = c
        row += 1
    instructions = input_source[row + 1]
    return map_dict, instructions


input_string = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
"""


def test_read_map():
    map_dict, instructions = read_map(input_string.splitlines())
    # assert map_dict == {(0, 3): '#', (1, 1): '#', (2, 0): '#', (3, 0): '.', (4, 3): '#', (5, 7): '#', (6, 8): '#', (7, 2): '#', (8, 4): '#', (9, 9): '#', (10, 3): '#', (11, 9): '#'}
    assert instructions == '10R5L5R10L4R5L5'
    return True


dirs = '>v<^'
directions = {'>': (0, 1), 'v': (1, 0), '<': (0, -1), '^': (-1, 0)}


# compute neighbor coordinates in each direction for every empty tile on the board, and store them in a dictionary
# coordinates of the next tile in the given direction are e.g.
# neighbors[(0, 7)]['>'] = (0, 8) - no wrapping
# neighbors[(0, 10)]['>'] = (0, 7) - wrapping around the right edge
def compute_neighbors(map_dict):
    neighbors = {}
    for (row, col), c in map_dict.items():
        if c == '.':
            neighbors[(row, col)] = {}
            for d, (dr, dc) in directions.items():
                if (row + dr, col + dc) in map_dict:
                    neighbors[(row, col)][d] = (row + dr, col + dc)
                else:  # wrap around
                    curr_row, curr_col = row, col
                    while (curr_row - dr, curr_col - dc) in map_dict:
                        curr_row -= dr
                        curr_col -= dc
                    neighbors[(row, col)][d] = (curr_row, curr_col)
    return neighbors


# Find the starting position
def find_start(map_dict):
    for (row, col), c in map_dict.items():
        if c == '.':
            return row, col


def test_find_start():
    map_dict, instructions = read_map(input_string.splitlines())
    assert find_start(map_dict) == (0, 8)


def solution22(input_source):
    map_dict, instructions = read_map(input_source.splitlines())
    neighbors = compute_neighbors(map_dict)
    row, col = find_start(map_dict)
    facing = 0  # 0 for right, 1 for down, 2 for left, 3 for up
    for instruction in split_instructions(instructions):
        if instruction in "RL":
            facing = (facing + 1 * (-1) ** (instruction == 'L')) % 4
        else:
            for _ in range(int(instruction)):
                next_row, next_col = neighbors[(row, col)][dirs[facing]]
                if map_dict[(next_row, next_col)] == '#':
                    break
                row, col = next_row, next_col
    return 1000 * (row + 1) + 4 * (col + 1) + facing  # 1-based indexing


# if __name__ == "__main__":
#     test_split_instructions()
#     map_dict, instructions = read_map(input_string.splitlines())
#     nbhd = compute_neighbors(map_dict)
#     # print(map_dict, "\n")
#     # print(nbhd)
#     print(solution22(input_string))
#     with open("22input.txt") as f:
#         print(solution22(f.read()))


# ___________________________ Part 2 ___________________________
# now the map is folded in a cube with 6 faces 50 x 50 tiles each,
# starting position remains the same, but the wrapping rules are different:
# 1. if the player moves off the edge of the current face, they are moved to the corresponding edge of the adjacent face
# 2. the direction has to be changed if the player moves from one face to another, but not if they move within a face
# 3. if the player moves to a wall, they stop before the wall
# This changes the way the neighbors are computed and makes additional entry
# for facing in the neighbors dictionary necessary
# my specific folding pattern is:
#  6622
#  6622
#  33
#  33
# 5511
# 5511
# 44
# 44
# where 1, 2, 3, 4, 5, 6 are the faces of the cube
#
# compute the neighbors for each tile on the cube
def compute_neighbors_cube(map_dict):
    cub_faces = "623514"

    def get_face(row, col):
        if 0 <= row < 50 and 50 <= col < 100:
            return 6
        elif 0 <= row < 50 and 100 <= col < 150:
            return 2
        elif 50 <= row < 100 and 50 <= col < 100:
            return 3
        elif 100 <= row < 150 and 0 <= col < 50:
            return 5
        elif 100 <= row < 150 and 50 <= col < 100:
            return 1
        elif 150 <= row < 200 and 0 <= col < 50:
            return 4
        else:
            raise RuntimeError(f"Invalid coordinates row {row}, col {col}")  # should never happen

    neighbors = {}
    for (row, col), char in map_dict.items():
        if char == '.':
            neighbors[(row, col)] = {}
            for d, (dr, dc) in directions.items():
                if (row + dr, col + dc) in map_dict:
                    neighbors[(row, col)][d] = (row + dr, col + dc), d
                else:  # wrap around
                    curr_face = get_face(row, col)
                    #new_face = get_face(row + dr, col + dc)
                    wrap = {(2, '>'): ('<', lambda r, c: (149 - r, c -  50)),
                            (1, '>'): ('<', lambda r, c: (149 - r, c +  50)),
                            (2, '^'): ('^', lambda r, c: (r + 199, c - 100)),
                            (4, 'v'): ('v', lambda r, c: (r - 199, c + 100)),
                            (2, 'v'): ('<', lambda r, c: (c - 50, r + 50)),
                            (3, '>'): ('^', lambda r, c: (c - 50, r + 50)),
                            (6, '^'): ('>', lambda r, c: (c + 100, 0)),
                            (4, '<'): ('v', lambda r, c: (0, r - 100)),
                            (6, '<'): ('>', lambda r, c: (149 - r, c - 50)),
                            (5, '<'): ('>', lambda r, c: (149 - r, 50)),
                            (3, '<'): ('v', lambda r, c: (100, r - 50)),
                            (5, '^'): ('>', lambda r, c: (c + 50, 50)),
                            (1, 'v'): ('<', lambda r, c: (c + 100, 49)),
                            (4, '>'): ('^', lambda r, c: (149, r - 100)),
                            }
                    new_direction, fn = wrap[(curr_face, d)]
                    curr_row, curr_col = fn(row, col)
                    try:
                        assert str(get_face(curr_row, curr_col)) in cub_faces
                    except:
                        p(f"from {row},{col} face {curr_face} in dir {d} got", curr_row, curr_col)
                        raise RuntimeError("Invalid coordinates")
                    neighbors[(row, col)][d] = (curr_row, curr_col), new_direction
    return neighbors

import sys
def p(*s):
    return
    print(*s, file=sys.stderr, flush=True)

def solution22_cube(input_source):
    map_dict, instructions = read_map(input_source.splitlines())
    neighbors = compute_neighbors_cube(map_dict)
    row, col = find_start(map_dict)
    facing = 0  # 0 for right, 1 for down, 2 for left, 3 for up
    for instruction in split_instructions(instructions):
        p((row,col), facing, instruction)
        if instruction in "RL":
            facing = (facing + 1 * (-1) ** (instruction == 'L')) % 4
        else:
            for _ in range(int(instruction)):
                (next_row, next_col), new_dir = neighbors[(row, col)][dirs[facing]]
                if map_dict[(next_row, next_col)] == '#':
                    break
                row, col = next_row, next_col
                facing = dirs.index(new_dir)
    p((row, col), facing)
    return 1000 * (row + 1) + 4 * (col + 1) + facing  # 1-based indexing


if __name__ == "__main__":
    # test_split_instructions()
    # map_dict, instructions = read_map(input_string.splitlines())
    # nbhd = compute_neighbors(map_dict)
    # # print(map_dict, "\n")
    # print(nbhd)
    #print(solution22_cube(input_string))
    with open("22input_empty.txt") as f:
        print(solution22_cube(f.read()))
        p("Should return to (0, 50) facing right. That way we know the cube is folded OK.")
    with open("22input.txt") as f:
        print("Part 2:", solution22_cube(f.read()))
