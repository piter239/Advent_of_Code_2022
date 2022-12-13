# using the solution of 13a.py, solve the
# --- Part Two ---
# Now, you just need to put all the packets in the right order. Disregard the blank lines in your list of received packets.
#
# The distress signal protocol also requires that you include two additional divider packets:
#
# [[2]]
# [[6]]
# Using the same rules as before, organize all packets - the ones in your list of received packets as well as the two divider packets - into the correct order.
#
# For the example above, the result of putting the packets in the correct order is:
#
# []
# [[]]
# [[[]]]
# [1,1,3,1,1]
# [1,1,5,1,1]
# [[1],[2,3,4]]
# [1,[2,[3,[4,[5,6,0]]]],8,9]
# [1,[2,[3,[4,[5,6,7]]]],8,9]
# [[1],4]
# [[2]]
# [3]
# [[4,4],4,4]
# [[4,4],4,4,4]
# [[6]]
# [7,7,7]
# [7,7,7,7]
# [[8,7,6]]
# [9]
# Afterward, locate the divider packets. To find the decoder key for this distress signal, you need to determine the indices of the two divider packets and multiply them together. (The first packet is at index 1, the second packet is at index 2, and so on.) In this example, the divider packets are 10th and 14th, and so the decoder key is 140.
#
# Organize all the packets into the correct order. What is the decoder key for the distress signal?

# Read the input file 13input.txt, and store the pairs of packets in a list
import solution13a  # solution13a.py contains the function read_input() and the function compare_packets()
packets = solution13a.read_input()

# transform list of pairs of packets into a list of packets
before = len(packets)
packets = [packet for pair in packets for packet in pair]
after = len(packets)
print("Transformed list of pairs of packets into a list of packets.  Before: %d pairs, after: %d packets" % (before, after))
if before * 2 != after:
    print("Error:  before * 2 != after")
    quit()

# Add the two divider packets to the list of packets.
# The divider packets are [[2]] and [[6]]
packets.append([[2]])
packets.append([[6]])

from functools import cmp_to_key
# sort the packets, using the compare function from solution13a.py
packets.sort(key=cmp_to_key(solution13a.compare))

# determine the indices of the two divider packets
divider1 = packets.index([[2]])
divider2 = packets.index([[6]])
# multiply the indices of the two divider packets, correcting for the fact that the indices are 0-based instead of 1-based
decoder_key = (divider1 + 1) * (divider2 + 1)
print("The decoder key is %d" % decoder_key)
print(*packets,sep='\n')

