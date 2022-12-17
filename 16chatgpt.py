def proboscidea_volcanium(flowRate, neighbors, runtime=30):
    # Define the dictionary dp[i][j] --> set((total_pressure: int, valve_j_opened_before_i: bool))
    # where i is the current time and
    # j is the current valve.
    # The values of paris in set dp[i][j] represent:
    # total_pressure -  the pressure that will be released by the valves opened before time i when time==runtime
    # valve_j_opened_before_i - True if valve j was opened before time i, False otherwise
    # It is a set, because there can be multiple ways to get to the same valve j at time i
    dp = {}
    dp[0] = {'AA': set((0, False))}
    # before time 0, no valve is opened, generated pressure is 0; only position AA is available

    # Iterate over the time from 0 to runtime-2 (as long as opening valves can make a difference).
    for i in range(runtime-1):
        # For each time i, iterate over all the valves in the dictionary d[i].
        for j in dp[i].keys():
            # iterate over each possible path in time i to valve, sorting by pressure?
            # or just iterate over the first path with the highest pressure?
            # different paths can have the same pressure, but different valves opened before time i
            for pressure, opened in sorted(dp[i][j], key=lambda x: x[0], reverse=True):
                # if the valve is opened before time i, we consider moving to the neighbors only
                if opened:
                    for neighbor in neighbors[j]:
                        dp[i + 1][neighbor].add = (pressure, opened)
                # if the valve is not opened before time i, we can open it and stay at the same position
                # or move to the neighbors without opening the valve
                # BIG PROBLEM: at the neighbors, we DO NOT know if the valve was opened before time i
                else:
                    update_neighbors(dp, i, j, neighbors[j])
                    # we can also open the valve at time i + 2 and update the pressure of the neighbors
                    if i + 2 <= runtime:
                        update_neighbors(dp, i + 2, j, neighbors[j])

    # The maximum pressure released overall would be the maximum of dp[i][j] for all i and j.
    result = get_max_pressure(dp, flowRate)

    return result






def get_max_pressure(dp, flowRate):
    result = 0
    for i in range(31):
        for j in flowRate:
            result = max(result, dp[i][j])
    return result

if __name__ == '__main__':
# Test the function with the example input
    flowRate = {'AA': 0, 'BB': 13, 'CC': 2, 'DD': 20, 'EE': 3, 'FF': 0, 'GG': 0, 'HH': 22, 'II': 0, 'JJ': 21}
    neighbors = {'AA': ['DD', 'II', 'BB'], 'BB': ['CC', 'AA'], 'CC': ['DD', 'BB'], 'DD': ['CC', 'AA', 'EE'],
                 'EE': ['FF', 'DD'], 'FF': ['EE', 'GG'], 'GG': ['FF', 'HH'], 'HH': ['GG'], 'II': ['AA', 'JJ'], 'JJ': ['II']}

    print(proboscidea_volcanium(flowRate, neighbors))  # Expected output: 364

""" MY TAKE ON PROBLEM 1 description

For example, suppose you had the following scan output:

Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II

All of the valves begin closed. You have 30 minutes to open valves and run tunnels. 
The goal is to maximize the total pressure released. 

At start you are standing at valve labeled AA.

It will take you one minute to open a single valve and one minute to follow any tunnel from one valve to another. 
After the valve is open, it will remain open for the rest of the simulation, releasing pressure at it's flow rate/minute. 

Write algorith in python to compute the maximum amount of pressure you could release.

                -------- ChatGPT take on the same task --------

Write a Python function that finds the maximum possible pressure release in a given cave system. The function should take in the following arguments:

valves: a dictionary representing the valve flow rates and connected tunnels. The keys of the dictionary are strings representing the valve names, and the values are tuples containing the flow rate (an integer) and a list of strings representing the connected valves.
time_limit: an integer representing the time limit for releasing pressure.
time_to_open: an integer representing the time needed to open a valve.
time_to_move: an integer representing the time needed to move between valves.
start_position: a string representing the starting valve.
The function should return an integer representing the maximum possible pressure release.

Example input is stored in an input file and should be read by the function.                

"""
