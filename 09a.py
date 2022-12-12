# solution to https://adventofcode.com/2022/day/9

# Here I used ChatGPT with following prompt
# Create a class Rope having internal head and tail position in 2d grid. A Rope is created on a starting position.
# A Rope can receive commands Up, Down, Left and Right and has to be able to track its position relative to starting position.
#
# The Rope must be quite short; in fact, the head (H) and tail (T) must always be touching
# (diagonally adjacent and even overlapping both count as touching).
#
# If the head is ever two steps directly up, down, left, or right from the tail,
# the tail must also move one step in that direction so it remains close enough.
#
# Otherwise, if the head and tail aren't touching and aren't in the same row or column, the tail always moves one step diagonally to keep up.
#
# Additionally, the number of cells visited by the tail at least once has to be tracked.
# A method get_visited_cells_number returns this number.
#
# Result:

class Rope:
    def __init__(self, starting_position=(0, 0)):
        self.head = starting_position
        self.tail = starting_position
        self.visited_cells = set()
        self.visited_cells.add(starting_position)

    def move_pos(self, dif_position):
        ''' dif_position is (dx, dy) from {-1,0,1} ** 2
        returns dif_position of the tail - for propagation'''
        assert(len(dif_position) == 2)
        assert(abs(dif_position[0]) <= 1 and abs(dif_position[1]) <= 1)

        # by all moves, including diagonal ones, dx and dy of head AND tail are in {-1,0,1}
        # while maintaining the abs distance between head and tail <= 1

        tail_head_dif = [0, 0]
        self.head = tuple(self.head[i] + dif_position[i] for i in range(2))
        tail_head_dif = [self.head[i] - self.tail[i] for i in range(2)]

        assert(abs(tail_head_dif[0]) + abs(tail_head_dif[1]) <= 3)

        if abs(tail_head_dif[0]) == 2 or abs(tail_head_dif[1]) == 2:
            for i in range(2):
                if tail_head_dif[i]:
                    tail_head_dif[i] = tail_head_dif[i]//abs(tail_head_dif[i])   # so that diff is in {-1,1}
            self.tail = tuple(self.tail[i] + tail_head_dif[i] for i in range(2))
            self.visited_cells.add(self.tail)

        return tuple(tail_head_dif)

    def __str__(self):
        # initialize the string with the starting position
        s = '' # "s"

        # get the minimum and maximum x and y coordinates of visited cells
        min_x = min([x for x, y in self.visited_cells] + [self.head[0]])
        max_x = max([x for x, y in self.visited_cells] + [self.head[0]])
        min_y = min([y for x, y in self.visited_cells] + [self.head[1]])
        max_y = max([y for x, y in self.visited_cells] + [self.head[1]])

        # loop over the rows and columns within the bounds of the visited cells
        for y in range(max_y, min_y - 1, -1):
            for x in range(min_x, max_x + 1):
                # add a '#' for visited cells, '.' for unvisited cells
                # 'H' for head, 'T' for tail
                if (x, y ) == self.head:
                    s += 'H'
                elif (x, y) == self.tail:
                    s += "T"
                elif (x, y) in self.visited_cells:
                    s += "#"
                else:
                    s += "."

            # add a newline character after each row
            s += "\n"
        # return the string representation of the Rope instance
        return s



    def get_visited_cells_number(self):
        return len(self.visited_cells)

# next prompt
#
# Now there is a file containing commands U, D, R, L with a counter.
# For example:
#
# R 4
# U 4
# L 3
# D 1
# R 4
# D 1
# L 5
# R 2
# This series of motions moves the head of Rope right four steps, then up four steps, then left three steps, then down one step, and so on.
#
# Write code to read from such text file and execute the commands


rope = Rope((0, 0))

# open the file
with open("09input.txt", "r") as f:
    # read each line of the file
    for line in f:
        # split the line into the command and the number of steps
        parts = line.strip().split(" ")
        command = parts[0]
        steps = int(parts[1])
        print(f'== {command} {steps} ==\n')
        # execute the command for the specified number of steps
        for _ in range(steps):
            dif_pos = (0, 0)
            if command == "U":
                dif_pos = (0, 1)
            elif command == "D":
                dif_pos = (0, -1)
            elif command == "L":
                dif_pos = (-1, 0)
            elif command == "R":
                dif_pos = (1, 0)
            rope.move_pos(dif_pos)
            #print(rope)
            #print()
# get the number of cells visited by the tail of the rope
visited_cells = rope.get_visited_cells_number()
print(visited_cells)
#print(rope)
