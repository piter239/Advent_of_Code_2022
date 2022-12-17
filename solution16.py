# read the input file "16input.txt" and return dictionary
import re


def read_file(filename="16input.txt"):
    valves = {}
    try:
        with open(filename) as f:
            for line in f:
                print(line)
                # use regular expressions to extract the valve name, flow rate, and neighbors
                valve_name, flow_rate, neighbors = re.search(
                    r'Valve (\w+) has flow rate=(\d+); tunnels lead to valves ([\w, ]+)', line).groups()
                valves[valve_name] = {'flow_rate': int(flow_rate), 'neighbors': neighbors.split(', ')}
    except:
        print("error")
    print(valves)
    return valves


def maximum_flow_rate(valves, time):
    # create a mapping from valve names to integer indices
    valve_name_to_index = {valve_name: i for i, valve_name in enumerate(valves)}

    # initialize the dp array with -1
    dp = [[-1 for j in range(time + 1)] for i in range(len(valves))]

    # fill in the dp array using the recursive formula
    for j in range(1, time + 1):
        for valve_name in valves:
            # skip valves with flow rate 0
            if valves[valve_name]['flow_rate'] == 0:
                continue
            for neighbor in valves[valve_name]['neighbors']:
                neighbor_index = valve_name_to_index[neighbor]
                valve_index = valve_name_to_index[valve_name]
                dp[valve_index][j] = max(dp[valve_index][j],
                                         dp[neighbor_index][j - 2] + valves[valve_name]['flow_rate'])

        # find the valve with the maximum flow rate after the given time
        max_valve, max_flow_rate = find_max_flow_rate(dp, valves, time)
        # reconstruct the path by backtracking through the dp array
        # path = reconstruct_path(dp, valves, max_valve, max_flow_rate, time)

        #return path, max_flow_rate
        return max_flow_rate


def find_max_flow_rate(dp, valves, time):
    max_valve = None
    max_flow_rate = 0
    for valve_name in valves:
        if dp[valve_name][time] > max_flow_rate:
            max_valve = valve_name
            max_flow_rate = dp[valve_name][time]
    return max_valve, max_flow_rate


def reconstruct_path(dp, valves, max_valve, max_flow_rate, time):
    path = []
    t = time
    while t > 0:
        path.append(max_valve)
        for neighbor in valves[max_valve]['neighbors']:
            if dp[neighbor][t - 2] + valves[max_valve]['flow_rate'] == max_flow_rate:
                max_valve = neighbor
                max_flow_rate -= valves[max_valve]['flow_rate']
                t -= 2
    return path


if __name__ == '__main__':
    valves = read_file()
    print(maximum_flow_rate(valves, 30))
