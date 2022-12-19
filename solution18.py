# Prompt used:
# pretend you are software architect. I will give you a problem description from customer, and you will rewrite it as a task for junior developer to work on.
#
# Here is the first description:
# and then the full task description out of https://adventofcode.com/2022/day/18

# RESULT
# Task for junior developer:
#
# You have been given a 3D grid of 1x1x1 cubes, each represented by its x,y,z position. Your task is to write a function
# that takes in this grid and returns the total surface area of the cubes.
#
# To calculate the surface area, count the number of sides of each cube that are not immediately connected to another cube.
# For example, if the grid contains two adjacent cubes such as 1,1,1 and 2,1,1, each cube would have a single side covered
# and five sides exposed, for a total surface area of 10 sides.
# A larger example is shown below:
# cubes = [(2, 2, 2), (1, 2, 2), (3, 2, 2), (2, 1, 2), (2, 3, 2), (2, 2, 1), (2, 2, 3),
#         (2, 2, 4), (2, 2, 6), (1, 2, 5), (3, 2, 5), (2, 1, 5), (2, 3, 5)]
# In the above example, after counting up all the sides that aren't connected to another cube,
# the total surface area is 64.

# Further, consider only cube sides that could be reached by the water and steam as the lava droplet tumbles into the pond.
# The steam will expand to reach as much as possible, completely displacing any air on the outside of the lava droplet
# but never expanding diagonally.
# In the larger example above, exactly one cube of air is trapped within the lava droplet (at 2,2,5),
# so the exterior surface area of the lava droplet is 58.


Neighborhood3D = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

# Use the provided example in the prompt to test your implementation.
# The calculate_surface_area function should return 64, and
# the calculate_surface_area_union should return 58 for the input:
cubes = [(2, 2, 2), (1, 2, 2), (3, 2, 2), (2, 1, 2), (2, 3, 2), (2, 2, 1), (2, 2, 3),
         (2, 2, 4), (2, 2, 6), (1, 2, 5), (3, 2, 5), (2, 1, 5), (2, 3, 5)]

cubes_original = cubes


def calculate_surface_area(cubes):
    surface_area = 0
    cube_set = set(cubes)
    # Iterate through each cube in the list of coordinates
    for i, cube in enumerate(cubes):
        # Initialize a count of exposed sides for this cube
        exposed_sides = 6
        # Check if any of the sides of this cube are connected to another cube
        for dx, dy, dz in Neighborhood3D:
            coord = (cube[0] + dx, cube[1] + dy, cube[2] + dz)
            # Check if the side is connected to another cube
            if coord in cube_set:
                exposed_sides -= 1

        # Add the number of exposed sides for this cube to the total surface area
        surface_area += exposed_sides
    return surface_area


# print(surface_area(cubes))
print("Example:", calculate_surface_area(cubes))


# PART 2

# union find solution

def get_air_neighbors(solid_cubes, x, y, z, d=1):
    ''''''
    neighbors = set()

    # Loop through each potential neighbor
    for dx, dy, dz in Neighborhood3D:
        # Calculate the coordinates of the neighbor
        nx, ny, nz = x + dx, y + dy, z + dz
        # Check if the neighbor is within the maximum distance
        if (nx, ny, nz) not in solid_cubes:
            neighbors.add((nx, ny, nz))
            if d > 1:
                neighbors |= get_air_neighbors(solid_cubes, nx, ny, nz, d - 1)

    return neighbors


def get_air_cubes(cubes, d=1):
    # Set of air cubes
    air_cubes = set()

    # Loop through each cube in the list
    for x, y, z in cubes:
        # Get the neighbors of the cube
        neighbors = get_air_neighbors(cubes, x, y, z, d)
        # Loop through each neighbor
        for nx, ny, nz in neighbors:
            # Check if the neighbor is not present in the list of cubes
            if (nx, ny, nz) not in cubes:
                # If the neighbor is not present, add it to the set of air cubes
                air_cubes.add((nx, ny, nz))

    return air_cubes


def add_air_cubes(air_cubes, d):
    # Set of air cubes to be added
    air_cubes_to_add = set()

    # Loop through each air cube in the set
    for x, y, z in air_cubes:
        # Get the neighbors of the air cube
        neighbors = get_air_neighbors(cubes, x, y, z, d)
        # Loop through each neighbor
        for nx, ny, nz in neighbors:
            # Check if the neighbor is not present in the set of air cubes
            if (nx, ny, nz) not in air_cubes:
                # If the neighbor is not present, add it to the set of air cubes to be added
                air_cubes_to_add.add((nx, ny, nz))

    # Add the air cubes to the original set
    air_cubes |= air_cubes_to_add

    return air_cubes


import unionfind

def cube_to_index(x, y, z):
    return x * 1000000 + y * 1000 + z
def index_to_cube(index):
    x = index // 1000000
    y = (index - x * 1000000) // 1000
    z = index - x * 1000000 - y * 1000
    return x, y, z

def calculate_surface_area_union(cubes, d):
    # Set of air cubes in the neighborhood of the lava cubes
    air_cubes = get_air_cubes(cubes, d)
    final_air_cubes = frozenset(air_cubes)
    # Union find data structure need integers as indices, and we need to map the coordinates to integers
    # We use a list to enumerate all the air cubes
    final_air_cubes_list = list(final_air_cubes)
    # and a dictionary to map the coordinates to the indices
    final_air_cubes_dict = {cube: i for i, cube in enumerate(final_air_cubes_list)}

    # Initialize the union find data structure
    # Create a unionFind object to track the disjoint subsets in the set of air cubes
    uf = unionfind.unionfind(len(final_air_cubes_list)) # air_cubes)
    # Loop through each air cube in the set
    for x, y, z in final_air_cubes_list:
        # Get the neighbors of the air cube
        neighbors = get_air_neighbors(cubes, x, y, z, 1)
        # Loop through each neighbor
        for nx, ny, nz in neighbors:
            # If the neighbor is in the set of air cubes, unite the two elements
            if (nx, ny, nz) in final_air_cubes:
                uf.unite(final_air_cubes_dict[x, y, z], final_air_cubes_dict[nx, ny, nz])
        # Determine the number of disjoint subsets in the set of air cubes
    enclosures = uf.groups()
    enclosures.sort(key=len)

    # heuristic: the largest enclosure is the one that contains the lava drops accessible from the outside
    # the others are enclosed within lava. So we only need to count
    # the surface area of cubes touching the largest air enclosure
    outside_enclosure_set = set(final_air_cubes_list[i] for i in enclosures[-1])
    # Loop through each air cube in this set
    surface_area = 0
    for x, y, z in outside_enclosure_set:
# Get the neighbors of the air cube
        for dx, dy, dz in Neighborhood3D:
            # Calculate the coordinates of the neighbor
            nx, ny, nz = x + dx, y + dy, z + dz
            # Check if the neighbor is present in the set of solid cubes
            if (nx, ny, nz) in cubes:
                # If the neighbor is present, add one to the surface area
                surface_area += 1
    return surface_area



#print("Union", calculate_surface_area_union(cubes, 2))
assert(calculate_surface_area_union(cubes, 2) == 58)

def read_cubes(filename='18input.txt'):
    cubes = []
    with open(filename) as f:
        for line in f:
            x, y, z = line.split(',')
            cubes.append((int(x), int(y), int(z)))
    return cubes


full_cubes = read_cubes()
print("Input:", calculate_surface_area(full_cubes))
print("Union", calculate_surface_area_union(full_cubes, 2))
