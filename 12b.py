# solution to https://adventofcode.com/2022/day/12

import numpy as np



# read the height map from URL https://adventofcode.com/2022/day/12/input




# read the heightmap from the text file
with open("12_heightmap.txt", "r") as f:
    heightmap = np.array([list(line.strip()) for line in f.readlines()])



# now all (a) and (S) are goals, and the (E) is the start position
start_row, start_col = np.where(heightmap == "E")
start_row = start_row[0]
start_col = start_col[0]
heightmap[start_row, start_col] = 'z'

goal_row, goal_col = np.where(heightmap == "S")
goal_row = goal_row[0]
goal_col = goal_col[0]
heightmap[goal_row, goal_col] = 'a'

# create a numpy array to store the distance to the goal at each position
distances = np.full_like(heightmap, np.iinfo(int).max, dtype=int)

# initialize the distance at the starting position to 0
distances[start_row, start_col] = 0

# create a queue to store the positions we need to visit
queue = [(start_row, start_col)]

# while there are positions left to visit
while queue:
    # pop the first position from the queue
    row, col = queue.pop(0)

    # get the current distance to the goal
    distance = distances[row, col]

    # for each of the 4 directions
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        # calculate the position of the neighboring square
        r, c = row + dr, col + dc

        # if the neighboring square is outside the heightmap, skip it
        if r < 0 or r >= heightmap.shape[0] or c < 0 or c >= heightmap.shape[1]:
            continue

        # if the neighboring square has already shorter path, skip it
        if distances[r, c] <= distance + 1:
            continue

        # if the neighboring square has an elevation more than 1 higher than the current square, skip it
        if -1 * (ord(heightmap[r, c]) - ord(heightmap[row, col])) > 1:
            continue

        # update the distance at the neighboring square
        distances[r, c] = distance + 1

        # add the neighboring square to the queue, if it is not a goal
        if heightmap[r,c] != 'a':
            queue.append((r, c))

# print the fewest number of steps required to move from the starting position to the goal position
print(distances[goal_row, goal_col])
print(distances)
print(heightmap)


# find the coordinates where heightmap is equal to 'a'
indices = np.where(heightmap == 'a')

# find the minimum value of distances at those coordinates
min_distance = distances[indices].min()

print(min_distance)

