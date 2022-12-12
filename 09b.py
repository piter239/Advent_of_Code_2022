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
    def __init__(self, starting_position=(0, 0), knots=2):
        self.knots = []
        for _ in range(knots):
            self.knots.append(starting_position)
        assert(len(self.knots) == knots)
        self.visited_cells = set()
        self.visited_cells.add(starting_position)

    def move_pos(self, dif_position):
        ''' dif_position is (dx, dy) from {-1,0,1} ** 2
        returns dif_position of the tail - for propagation'''
        assert(len(dif_position) == 2)
        assert(abs(dif_position[0]) <= 1 and abs(dif_position[1]) <= 1)

        # by all moves, including diagonal ones, dx and dy of head AND tail are in {-1,0,1}
        # while maintaining the abs distance between head and tail <= 1

        i = 0
        self.knots[i] = tuple(self.knots[i][d] + dif_position[d] for d in range(2))

        while i+1 < len(self.knots):
            tail_head_dif = [self.knots[i][d] - self.knots[i+1][d] for d in range(2)]
            tail_move = [0, 0]
            if abs(tail_head_dif[0]) == 2 or 2 == abs(tail_head_dif[1]):
                for d in range(2):
                    if tail_head_dif[d]:
                        tail_move[d] = tail_head_dif[d]//abs(tail_head_dif[d])   # so that diff is in {-1,1}
                self.knots[i+1] = tuple(self.knots[i+1][d] + tail_move[d] for d in range(2))
            else:
                break
            i += 1

        self.visited_cells.add(self.knots[-1])

    def __str__(self):
        # initialize the string with the starting position
        s = '' # "s"

        # get the minimum and maximum x and y coordinates of visited cells
        min_x = min([x for x, y in self.visited_cells] + [x for x, y in self.knots])
        max_x = max([x for x, y in self.visited_cells] + [x for x, y in self.knots])
        min_y = min([y for x, y in self.visited_cells] + [y for x, y in self.knots])
        max_y = max([y for x, y in self.visited_cells] + [y for x, y in self.knots])

        # loop over the rows and columns within the bounds of the visited cells
        for y in range(max_y, min_y - 1, -1):
            for x in range(min_x, max_x + 1):
                # add a '#' for visited cells, '.' for unvisited cells
                # 'H' for head, 'T' for tail
                if (x, y ) in self.knots:
                    s += str(self.knots.index((x,y)))
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



# now I want to connect ten ropes, named from 0 to 9, so that the head of  each rope i
# from 1 to 9 is always exactly at the same position as the tail from rope i-1
#
# the goal is to calculate the number of cells, visited by the tail of last rope,
# that is the rope number 9
#
# I want the head of the rope 1 to be at the position of the tail of rope 0,
# the head of rope 2 to be at the position of the tail of rope 1 etc.
#
# The head of rope 9 is always at the position of the tail of rope 8.


ropes = Rope((0, 0), 10)

# open the file
with open("09input.txt", "r") as f:
    # read each line of the file
    for line in f:
        # split the line into the command and the number of steps
        parts = line.strip().split(" ")
        command = parts[0]
        steps = int(parts[1])

        print(f'== {command} {steps} ==\n')

        # execute the command for the specified number of steps,
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
            ropes.move_pos(dif_pos)

            #print(ropes)


# get the number of cells visited by the tail of the last rope (rope 9)
visited_cells = ropes.get_visited_cells_number()
print(visited_cells)

print(ropes)
