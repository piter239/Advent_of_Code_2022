# --- Day 15: Beacon Exclusion Zone ---
# You feel the ground rumble again as the distress signal leads you to a large network of subterranean tunnels.
# You don't have time to search them all, but you don't need to: your pack contains a set of deployable sensors that
# you imagine were originally built to locate lost Elves.
#
# The sensors aren't very powerful, but that's okay; your handheld device indicates that you're close enough to the
# source of the distress signal to use them. You pull the emergency sensor system out of your pack, hit the big button
# on top, and the sensors zoom off down the tunnels.
#
# Once a sensor finds a spot it thinks will give it a good reading, it attaches itself to a hard surface and begins
# monitoring for the nearest signal source beacon. Sensors and beacons always exist at integer coordinates.
# Each sensor knows its own position and can determine the position of a beacon precisely; however, sensors can only
# lock on to the one beacon closest to the sensor as measured by the Manhattan distance.
# (There is never a tie where two beacons are the same distance to a sensor.)
#
# It doesn't take long for the sensors to report back their positions and closest beacons (your puzzle input).
# For example:
#
# Sensor at x=2, y=18: closest beacon is at x=-2, y=15
# Sensor at x=9, y=16: closest beacon is at x=10, y=16
# Sensor at x=13, y=2: closest beacon is at x=15, y=3
# Sensor at x=12, y=14: closest beacon is at x=10, y=16
# Sensor at x=10, y=20: closest beacon is at x=10, y=16
# Sensor at x=14, y=17: closest beacon is at x=10, y=16
# Sensor at x=8, y=7: closest beacon is at x=2, y=10
# Sensor at x=2, y=0: closest beacon is at x=2, y=10
# Sensor at x=0, y=11: closest beacon is at x=2, y=10
# Sensor at x=20, y=14: closest beacon is at x=25, y=17
# Sensor at x=17, y=20: closest beacon is at x=21, y=22
# Sensor at x=16, y=7: closest beacon is at x=15, y=3
# Sensor at x=14, y=3: closest beacon is at x=15, y=3
# Sensor at x=20, y=1: closest beacon is at x=15, y=3
# So, consider the sensor at 2,18; the closest beacon to it is at -2,15. For the sensor at 9,16, the closest beacon
# to it is at 10,16.
#
# Drawing sensors as S and beacons as B, the above arrangement of sensors and beacons looks like this:
#
#                1    1    2    2
#      0    5    0    5    0    5
#  0 ....S.......................
#  1 ......................S.....
#  2 ...............S............
#  3 ................SB..........
#  4 ............................
#  5 ............................
#  6 ............................
#  7 ..........S.......S.........
#  8 ............................
#  9 ............................
# 10 ....B.......................
# 11 ..S.........................
# 12 ............................
# 13 ............................
# 14 ..............S.......S.....
# 15 B...........................
# 16 ...........SB...............
# 17 ................S..........B
# 18 ....S.......................
# 19 ............................
# 20 ............S......S........
# 21 ............................
# 22 .......................B....
# This isn't necessarily a comprehensive map of all beacons in the area, though. Because each sensor only identifies
# its closest beacon, if a sensor detects a beacon, you know there are no other beacons that close or closer to that
# sensor. There could still be beacons that just happen to not be the closest beacon to any sensor.
# Consider the sensor at 8,7:
#
#                1    1    2    2
#      0    5    0    5    0    5
# -2 ..........#.................
# -1 .........###................
#  0 ....S...#####...............
#  1 .......#######........S.....
#  2 ......#########S............
#  3 .....###########SB..........
#  4 ....#############...........
#  5 ...###############..........
#  6 ..#################.........
#  7 .#########S#######S#........
#  8 ..#################.........
#  9 ...###############..........
# 10 ....B############...........
# 11 ..S..###########............
# 12 ......#########.............
# 13 .......#######..............
# 14 ........#####.S.......S.....
# 15 B........###................
# 16 ..........#SB...............
# 17 ................S..........B
# 18 ....S.......................
# 19 ............................
# 20 ............S......S........
# 21 ............................
# 22 .......................B....
# This sensor's closest beacon is at 2,10, and so you know there are no beacons that close or closer
# (in any positions marked #).
#
# None of the detected beacons seem to be producing the distress signal, so you'll need to work out where the distress
# beacon is by working out where it isn't. For now, keep things simple by counting the positions where a beacon cannot
# possibly be along just a single row.
#
# So, suppose you have an arrangement of beacons and sensors like in the example above and, just in the row where y=10,
# you'd like to count the number of positions a beacon cannot possibly exist. The coverage from all sensors near that
# row looks like this:
#
#                  1    1    2    2
#        0    5    0    5    0    5
#  9 ...#########################...
# 10 ..####B######################..
# 11 .###S#############.###########.
# In this example, in the row where y=10, there are 26 positions where a beacon cannot be present.
#
# Consult the report from the sensors you just deployed. In the row where y=2000000, how many positions cannot
# contain a beacon?


import re


def read_input():
    # Open the input file
    with open("15input.txt", "r") as input_file:
        # Initialize an empty dictionary to store the sensor and beacon positions
        positions = {}
        # Compile a regular expression to match the sensor and beacon positions in the input file
        pattern = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")
        # Iterate over the lines in the file
        for line in input_file:
            # Use the regular expression to match the sensor and beacon positions in the line
            match = pattern.match(line)
            if match:
                # Extract the sensor and beacon positions from the match
                sensor_x, sensor_y, beacon_x, beacon_y = map(int, match.groups())
                # Add the sensor and beacon positions to the dictionary, with the x and y coordinates as the key
                positions[(sensor_x, sensor_y)] = (beacon_x, beacon_y)
    # Return the dictionary of sensor and beacon positions
    return positions


# print out the positions of the sensors and beacons
def print_grid(positions, row=None):
    """if row is None, print the entire grid, otherwise print just the row"""

    sensors = positions.keys()
    beacons = set(positions.values())
    # Find the minimum and maximum x coordinates of the sensors and beacons
    min_x = min(point[0] for point in sensors | beacons)
    max_x = max(point[0] for point in sensors | beacons)
    min_y = min(point[1] for point in sensors | beacons)
    max_y = max(point[1] for point in sensors | beacons)

    # Print the grid
    for y in range(min_y, max_y + 1) if not row else [row]:
        # Print the grid row
        print(f"{y:>{len(str(max_y))}}: ", end="")

        for x in range(min_x, max_x + 1):
            # Print the sensor or beacon at the current position, or a dot if there is none
            if (x, y) in sensors:
                print("S", end="")
            elif (x, y) in beacons:
                print("B", end="")
            else:
                print(".", end="")
        print()
    return

# calculate Manhattan distance between two points
def dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


# count the number of positions where a beacon CANNOT be present in a row
def count_impossible_positions(positions, row):
    """y - the y-coordinate of the row to count positions in"""
    # Sets of sensor and beacon positions
    sensors = positions.keys()
    beacons = set(positions.values())
    # Find the minimum and maximum x coordinates of the sensors and beacons
    min_x = min(sensor[0] for sensor in sensors | beacons)
    max_x = max(sensor[0] for sensor in sensors | beacons)

    # Initialize a set of positions where a beacon cannot be present
    possible_positions = set()
    impossible_positions = set()
    counter = 0
    # Iterate over the x coordinates
    for x in range(min_x, max_x + 1):
        if any(dist(sensor, (x, row)) <= dist(positions[sensor], sensor) for sensor in sensors):
            if (x, row) not in beacons:
                #impossible_positions.add((x, row))
                counter += 1
    return counter


# count the number of positions where a beacon cannot be present in a row for the given input
def part1():
    # Read the input
    positions = read_input()
    #print_grid(positions)

    points = positions.keys() | positions.values()
    # Count the number of positions where a beacon cannot be present in the given row
    # first, count the total number of positions in the row
    min_x = min(point[0] for point in points)
    max_x = max(point[0] for point in points)

    total_positions =  max_x - min_x + 1

    roi = 10    # row of interest
    impossible_pos = count_impossible_positions(positions, roi)

    print("Impossible positions", impossible_pos)
    #print_grid(positions, roi)

    # print(f"{roi:>2}: ", end="")
    # for x in range(min_x, max_x + 1):
    #     # Print # if beacon impossible . otherwise
    #     res = "#" if (x, roi) in impossible_pos else "."
    #     print(res, end="")
    # print()


if __name__ == "__main__":
    part1()
