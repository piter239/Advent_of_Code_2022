# solution to https://adventofcode.com/2022/day/13
# --- Day 13: Distress Signal ---
# You climb the hill and again try contacting the Elves. However, you instead receive a signal you weren't expecting: a distress signal.
#
# Your handheld device must still not be working properly; the packets from the distress signal got decoded out of order. You'll need to re-order the list of received packets (your puzzle input) to decode the message.
#
# Your list consists of pairs of packets; pairs are separated by a blank line. You need to identify how many pairs of packets are in the right order.
#
# For example:
#
# [1,1,3,1,1]
# [1,1,5,1,1]
#
# [[1],[2,3,4]]
# [[1],4]
#
# [9]
# [[8,7,6]]
#
# [[4,4],4,4]
# [[4,4],4,4,4]
#
# [7,7,7,7]
# [7,7,7]
#
# []
# [3]
#
# [[[]]]
# [[]]
#
# [1,[2,[3,[4,[5,6,7]]]],8,9]
# [1,[2,[3,[4,[5,6,0]]]],8,9]
# Packet data consists of lists and integers. Each list starts with [, ends with ], and contains zero or more comma-separated values (either integers or other lists). Each packet is always a list and appears on its own line.
#
# When comparing two values, the first value is called left and the second value is called right. Then:
#
# If both values are integers, the lower integer should come first. If the left integer is lower than the right integer, the inputs are in the right order. If the left integer is higher than the right integer, the inputs are not in the right order. Otherwise, the inputs are the same integer; continue checking the next part of the input.
# If both values are lists, compare the first value of each list, then the second value, and so on. If the left list runs out of items first, the inputs are in the right order. If the right list runs out of items first, the inputs are not in the right order. If the lists are the same length and no comparison makes a decision about the order, continue checking the next part of the input.
# If exactly one value is an integer, convert the integer to a list which contains that integer as its only value, then retry the comparison. For example, if comparing [0,0,0] and 2, convert the right value to [2] (a list containing 2); the result is then found by instead comparing [0,0,0] and [2].
#
# What are the indices of the pairs that are already in the right order? (The first pair has index 1, the second pair has index 2, and so on.) In the above example, the pairs in the right order are 1, 2, 4, and 6; the sum of these indices is 13.
#
# Determine which pairs of packets are already in the right order. What is the sum of the indices of those pairs?

# Read the input file 13input.txt, and store the pairs of packets in a list
# of lists, where each list contains two packets.   Each packet is a list
# of integers and lists.        The packets are separated by a blank line.
# The input file is in the same directory as this program.
def read_input():
    with open("13input.txt", "r") as f:
        # Read all the lines of the file, and store them in a list.
        # Each line is a string.
        lines = f.readlines()

        # Each packet is a list of integers and lists.
        # Each packet is stored in a list.
        # Each pair of packets is stored in a list.
        # All the pairs of packets are stored in a list.
        packets = []

        # The current pair of packets is a list of two lines.
        current_pair = []

        # Loop through all the lines of the input file.
        for line in lines:
            # Remove the newline character from the end of the line.
            line = line.strip()

            # If the line is empty, then it is the separator between
            # pairs of packets.
            if line == "":
                # Add the current pair of packets to the list of pairs of packets.
                if len(current_pair) == 2:
                    packets.append(current_pair)
                    current_pair = []
                else:
                    print("Error: current_pair is not a pair of packets.")
                    quit()

            else:
                # The line is not empty, so it is a packet.
                # Convert the line to a list.
                current_pair.append(eval(line))

        return packets

# Compare two packets, and return True if the packets are in the right order.
# Otherwise, return False.
def compare_packets(left_packet, right_packet):

    # use recursive helper function compare returning
    # -1 if left_packet < right_packet
    # 0 if left_packet == right_packet
    # 1 if left_packet > right_packet
    # to compare two lists or integer with a list
    def compare(left_packet, right_packet):
        def sign(x):
            return (0, (1, -1)[x < 0])[x != 0]
        # If both packets are integers, compare them.
        if isinstance(left_packet, int) and isinstance(right_packet, int):
            return sign(left_packet - right_packet)
        # If both packets are lists,
        # then compare the first element of each list, then the second element,
        # and so on.
        if isinstance(left_packet, list) and isinstance(right_packet, list):
            # If either is empty
            if len(left_packet) == 0 or len(right_packet) == 0:
                return sign(len(left_packet) - len(right_packet))
            # If neither is empty, compare the first element of each list.
            # Compare the first element of each list.
            if compare(left_packet[0], right_packet[0]):
                return compare(left_packet[0], right_packet[0])
            else:
                # The first elements are the same, so compare the rest of the lists.
                return compare(left_packet[1:], right_packet[1:])
        # If one packet is a list and the other is an integer,
        # then convert the integer to a list containing that integer.
        if isinstance(left_packet, int):
            return compare([left_packet], right_packet)
        else:
            return compare(left_packet, [right_packet])
        print("Error: compare_packets: left_packet and right_packet are not packets.")
        quit()

    return compare(left_packet, right_packet) <= 0

# Determine which pairs of packets are already in the right order.
packets = read_input()

indices = [i for i in range(1, len(packets) + 1) if compare_packets(packets[i - 1][0], packets[i - 1][1])]
print(sum(indices))
