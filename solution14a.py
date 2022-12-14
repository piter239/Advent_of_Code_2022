# --- Day 14: Regolith Reservoir ---
# The distress signal leads you to a giant waterfall! Actually, hang on - the signal seems like it's coming from the waterfall itself, and that doesn't make any sense. However, you do notice a little path that leads behind the waterfall.
#
# Correction: the distress signal leads you behind a giant waterfall! There seems to be a large cave system here, and the signal definitely leads further inside.
#
# As you begin to make your way deeper underground, you feel the ground rumble for a moment. Sand begins pouring into the cave! If you don't quickly figure out where the sand is going, you could quickly become trapped!
#
# Fortunately, your familiarity with analyzing the path of falling material will come in handy here. You scan a two-dimensional vertical slice of the cave above you (your puzzle input) and discover that it is mostly air with structures made of rock.
#
# Your scan traces the path of each solid rock structure and reports the x,y coordinates that form the shape of the path, where x represents distance to the right and y represents distance down. Each path appears as a single line of text in your scan. After the first point of each path, each point indicates the end of a straight horizontal or vertical line to be drawn from the previous point. For example:
#
# 498,4 -> 498,6 -> 496,6
# 503,4 -> 502,4 -> 502,9 -> 494,9
# This scan means that there are two paths of rock; the first path consists of two straight lines, and the second path consists of three straight lines. (Specifically, the first path consists of a line of rock from 498,4 through 498,6 and another line of rock from 498,6 through 496,6.)
#
# The sand is pouring into the cave from point 500,0.
#
# Drawing rock as #, air as ., and the source of the sand as +, this becomes:
#
#
#   4     5  5
#   9     0  0
#   4     0  3
# 0 ......+...
# 1 ..........
# 2 ..........
# 3 ..........
# 4 ....#...##
# 5 ....#...#.
# 6 ..###...#.
# 7 ........#.
# 8 ........#.
# 9 #########.
# Sand is produced one unit at a time, and the next unit of sand is not produced until the previous unit of sand comes to rest. A unit of sand is large enough to fill one tile of air in your scan.
#
# A unit of sand always falls down one step if possible. If the tile immediately below is blocked (by rock or sand), the unit of sand attempts to instead move diagonally one step down and to the left. If that tile is blocked, the unit of sand attempts to instead move diagonally one step down and to the right. Sand keeps moving as long as it is able to do so, at each step trying to move down, then down-left, then down-right. If all three possible destinations are blocked, the unit of sand comes to rest and no longer moves, at which point the next unit of sand is created back at the source.
#
# So, drawing sand that has come to rest as o, the first unit of sand simply falls straight down and then stops:
#
# ......+...
# ..........
# ..........
# ..........
# ....#...##
# ....#...#.
# ..###...#.
# ........#.
# ......o.#.
# #########.
# The second unit of sand then falls straight down, lands on the first one, and then comes to rest to its left:
#
# ......+...
# ..........
# ..........
# ..........
# ....#...##
# ....#...#.
# ..###...#.
# ........#.
# .....oo.#.
# #########.
# After a total of five units of sand have come to rest, they form this pattern:
#
# ......+...
# ..........
# ..........
# ..........
# ....#...##
# ....#...#.
# ..###...#.
# ......o.#.
# ....oooo#.
# #########.
# After a total of 22 units of sand:
#
# ......+...
# ..........
# ......o...
# .....ooo..
# ....#ooo##
# ....#ooo#.
# ..###ooo#.
# ....oooo#.
# ...ooooo#.
# #########.
# Finally, only two more units of sand can possibly come to rest:
#
# ......+...
# ..........
# ......o...
# .....ooo..
# ....#ooo##
# ...o#ooo#.
# ..###ooo#.
# ....oooo#.
# .o.ooooo#.
# #########.
# Once all 24 units of sand shown above have come to rest, all further sand flows out the bottom, falling into the endless void. Just for fun, the path any new sand takes before falling forever is shown here with ~:
#
# .......+...
# .......~...
# ......~o...
# .....~ooo..
# ....~#ooo##
# ...~o#ooo#.
# ..~###ooo#.
# ..~..oooo#.
# .~o.ooooo#.
# ~#########.
# ~..........
# ~..........
# ~..........
# Using your scan, simulate the falling sand. How many units of sand come to rest before sand starts flowing into the abyss below?

# Read the input file 14input.txt with the cave map of form:
# 498,4 -> 498,6 -> 496,6
# 503,4 -> 502,4 -> 502,9 -> 494,9
def read_input():
    with open('14inputS.txt') as f:
        return f.read().splitlines()


# Create a dictionary of the cave map with the key being the x,y coordinate and the value being the character at that coordinate
# the input
# 498,4 -> 498,6 -> 496,6
# 503,4 -> 502,4 -> 502,9 -> 494,9
# becomes
#   4     5  5
#   9     0  0
#   4     0  3
# 0 ......+...
# 1 ..........
# 2 ..........
# 3 ..........
# 4 ....#...##
# 5 ....#...#.
# 6 ..###...#.
# 7 ........#.
# 8 ........#.
# 9 #########.
def create_cave_map():
    cave_map = {}
    for line in read_input():
        xp, yp = None, None  # previous x and y coordinates
        for i, pair in enumerate(line.split(' -> ')):
            x, y = map(int, pair.split(','))  # convert the x,y coordinate to integers
            cave_map[(x, y)] = '#'
            if i:
                if xp == x:
                    for y in range(min(yp, y), max(yp, y)):
                        cave_map[(x, y)] = '#'
                else:
                    for x in range(min(xp, x), max(xp, x)):
                        cave_map[(x, y)] = '#'
            xp, yp = x, y
    # fill in the air above the cave map and the + at the source of the sand
    # set the + at 500, 0 after filling the top row with .
    # find the min and max x and y coordinates
    min_x = min(cave_map.keys(), key=lambda x: x[0])[0]
    max_x = max(cave_map.keys(), key=lambda x: x[0])[0]
    min_y = min(cave_map.keys(), key=lambda x: x[1])[1]
    max_y = max(cave_map.keys(), key=lambda x: x[1])[1]
    # fill the top row with .
    for x in range(min_x, max_x + 1):
        for y in range(0, min_y):
            cave_map[(x, y)] = '.'
    cave_map[(500, 0)] = '+'  # set the + at 500, 0
    return cave_map


# test the create_cave_map function
# print to the stderr
import sys


def print_debug(*args, **kwargs):
    print(*args, file=sys.stderr, flush=True, **kwargs)


# print the cave map
def print_cave_map(cave_map):
    # find the min and max x and y coordinates
    min_x = min(cave_map.keys(), key=lambda x: x[0])[0]
    max_x = max(cave_map.keys(), key=lambda x: x[0])[0]
    min_y = min(cave_map.keys(), key=lambda x: x[1])[1]
    max_y = max(cave_map.keys(), key=lambda x: x[1])[1]

    # print the header
    left_margin = ' ' * (len(str(max_y)) + 1)
    top_margin = len(str(max_x))
    for y in range(top_margin):
        print_debug(left_margin, end='')
        for x in range(min_x, max_x + 1):
            if x in {500, min_x, max_x}:
                print_debug(str(x)[y], end='')
            else:
                print_debug(' ', end='')
        print_debug()

    # print the cave map
    for y in range(min_y, max_y + 1):
        print_debug('{:>{}} '.format(y, len(str(max_y))), end='')
        for x in range(min_x, max_x + 1):
            print_debug(cave_map.get((x, y), '.'), end='')
        print_debug()


# test the print_cave_map function
def test_print_cave_map():
    map = create_cave_map()
    print_cave_map(map)


test_print_cave_map()

free_space = set('./\\')

# simulate the falling sand
def simulate_falling_sand():
    map = create_cave_map()
    # find the min and max x and y coordinates
    min_x = min(map.keys(), key=lambda p: p[0])[0]
    max_x = max(map.keys(), key=lambda p: p[0])[0]
    min_y = min(map.keys(), key=lambda p: p[1])[1]
    max_y = max(map.keys(), key=lambda p: p[1])[1]

    source = (500, 0)
    map[source] = '.'   # unified handling of the source of the sand
    sand_count = 0      # count the number of sand units that come to rest
    last_sand_fall_to_abyss = False  # flag to indicate that the last sand fall was into the abyss
    x, y = source
    while map[source] != '*':  # while the source of the sand is not marked as * for sand
        while y <= max_y and map.get((x, y + 1), '.') in free_space:  # while the sand can fall down
            y += 1
        if y > max_y:  # if the sand fell into the abyss
            if not last_sand_fall_to_abyss:
                last_sand_fall_to_abyss = True
                x, y = source  # reset the x and y coordinates to the source of the sand
                continue
            else:
                break  # this is the second time the sand fell into the abyss in a row so stop the simulation

        if map.get((x - 1, y + 1), '.') in free_space:  # if the sand can fall left
            map[(x, y)] = '/'  # mark the sand as falling left
            x -= 1
            y += 1
        elif map.get((x + 1, y + 1), '.') in free_space: # if the sand can fall right
            map[(x, y)] = '\\'  # mark the sand as falling right
            x += 1
            y += 1
        else:  # the sand can't fall left or right so it comes to rest
            last_sand_fall_to_abyss = False
            map[(x, y)] = '*'  # mark the sand as * for sand
            sand_count += 1
            x, y = source  # reset the x and y coordinates to the source of the sand

    print_cave_map(map)
    return sand_count

def do_part1():
    print(simulate_falling_sand())

do_part1()


