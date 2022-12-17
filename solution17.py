# --- Day 17: Pyroclastic Flow ---
# Your handheld device has located an alternative exit from the cave for you and the elephants. The ground is rumbling almost continuously now, but the strange valves bought you some time. It's definitely getting warmer in here, though.
#
# The tunnels eventually open into a very tall, narrow chamber. Large, oddly-shaped rocks are falling into the chamber from above, presumably due to all the rumbling. If you can't work out where the rocks will fall next, you might be crushed!
#
# The five types of rocks have the following peculiar shapes, where # is rock and . is empty space:
#
# ####
#
# .#.
# ###
# .#.
#
# ..#
# ..#
# ###
#
# #
# #
# #
# #
#
# ##
# ##
# The rocks fall in the order shown above: first the - shape, then the + shape, and so on. Once the end of the list is
# reached, the same order repeats: the - shape falls first, sixth, 11th, 16th, etc.
#
# The rocks don't spin, but they do get pushed around by jets of hot gas coming out of the walls themselves.
# A quick scan reveals the effect the jets of hot gas will have on the rocks as they fall (your puzzle input).
#
# For example, suppose this was the jet pattern in your cave:
#
# >>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
# In jet patterns, < means a push to the left, while > means a push to the right. The pattern above means that
# the jets will push a falling rock right, then right, then right, then left, then left, then right, and so on.
# If the end of the list is reached, it repeats.
#
# The tall, vertical chamber is exactly 7 units wide.
#
# Each rock appears so that its left edge is 2 units away from the left wall
# and its bottom edge is 3 units above the highest rock in the room (or the floor, if there isn't one).
#
# After a rock appears, it alternates between being pushed by a jet of hot gas one unit (in the direction indicated by
# the next symbol in the jet pattern) and then falling one unit down. If any movement would cause any part of the rock
# to move into the walls, floor, or a stopped rock, the movement instead does not occur. If a downward movement
# would have caused a falling rock to move into the floor or an already-fallen rock, the falling rock stops where it is
# (having landed on something) and a new rock immediately begins falling.

# To prove to the elephants your simulation is accurate, they want to know how tall the tower will get after 2022 rocks
# have stopped (but before the 2023rd rock begins falling). In this example, the tower of rocks will be 3068 units tall.
#
# How many units tall will the tower of rocks be after 2022 rocks have stopped falling?


# read the input from file 17input.txt
def read_input():
    with open('17input.txt') as f:
        return f.read().strip()


# print(len(read_input()))

rocks = [['####'],
         ['.#.',
          '###',
          '.#.'],
         ['###',
          '..#',
          '..#'],
         ['#', '#', '#', '#'],
         ['##',
          '##']]

print(rocks)


def simulate_falling_rocks(pieces=2022, pattern='>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'):
    pit = [['#'] * 9] + [['#'] + ['.'] * 7 + ['#'] for _ in range(7)]  # pit[0] is the floor

    def print_pit(pit):
        for j in range(len(pit) - 1, -1, -1):
            print(''.join(pit[j]))

    def initial_position(pit, rock, height):
        """ calculate the initial positions of the rocks in the pit
        Each rock appears so that its left edge is 2 units away from the left wall
        and its bottom edge is 3 units above the highest rock in the room (or the floor, if there isn't one).
        """
        if len(rock) + 3 + height > len(pit) - 1:
            pit += [['#'] + ['.'] * 7 + ['#'] for _ in range(len(rock) + 3 + height + 7 - len(pit))]

        return 3, height + 3 + len(rock)

    def check_pos(pit, rock, pos) -> bool:
        """ check if the rock can be placed in the pit at the given position """
        for i in range(len(rock)):
            for j in range(len(rock[i])):
                if rock[i][j] == '#' and pit[pos[1] + i - len(rock) + 1][pos[0] + j] != '.':
                    return False
        return True

    def place_rock(pit, rock, pos):
        """ place the rock in the pit at the given position
            call AFTER checking if the rock can be placed in the pit at the given position"""
        for i in range(len(rock)):
            for j in range(len(rock[i])):
                if rock[i][j] == '#':
                    pit[pos[1] + i - len(rock) + 1][pos[0] + j] = '#'

    def remove_rock(pit, rock, pos):
        """ remove the rock from the pit at the given position """
        for i in range(len(rock)):
            for j in range(len(rock[i])):
                if rock[i][j] == '#':
                    pit[pos[1] + i - len(rock) + 1][pos[0] + j] = '.'

    def move_rock(pit, rock, pos, direction):
        """ move the rock in the given direction """
        from_pos = pos
        if direction == '>':
            pos = (pos[0] + 1, pos[1])
        elif direction == '<':
            pos = (pos[0] - 1, pos[1])
        elif direction == 'v':
            pos = (pos[0], pos[1] - 1)
        else:
            raise ValueError('Unknown direction: ' + direction)
        remove_rock(pit, rock, from_pos)
        if not check_pos(pit, rock, pos):
            place_rock(pit, rock, from_pos)
            return from_pos
        place_rock(pit, rock, pos)

        return pos

    height = 0  # current height of the tower
    pattern_pos = 0  # current position in the pattern
    for i in range(pieces):

        rock = rocks[i % len(rocks)]
        cpos = initial_position(pit, rock, height)
        # print('initial position:', cpos)
        if not check_pos(pit, rock, cpos):
            # print_pit(pit)
            raise ValueError('Rock does not fit in the pit')
        place_rock(pit, rock, cpos)
        # print('piece', i, 'height', height, 'cpos', cpos, 'pos:', pattern_pos, pattern[pattern_pos])
        # print_pit(pit)

        stop = False
        while not stop:
            direction = pattern[pattern_pos]
            pattern_pos = (pattern_pos + 1) % len(pattern)
            cpos = move_rock(pit, rock, cpos, direction)
            direction = 'v'
            old_pos = cpos
            cpos = move_rock(pit, rock, cpos, direction)
            if cpos == old_pos:
                stop = True
                height = max(height, cpos[1])
            # print_pit(pit)
            # remove_rock(pit, rock, cpos)
            # stop = True
    return height


if __name__ == '__main__':
    print(simulate_falling_rocks(pieces=2022, pattern=read_input()))
