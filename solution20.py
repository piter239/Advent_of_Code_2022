# You have been given an encrypted file containing a list of numbers.
# The file needs to be decrypted using a process called "mixing".
# To mix the file, you need to move each number forward or backward in the file a number of positions
# equal to the value of the number being moved. The list is circular, so moving a number off one end of the list
# wraps back around to the other end as if the ends were connected.
#
# The numbers should be moved in the order they originally appear in the encrypted file.
#
# After the mixing process, you need to find the 1000th, 2000th, and 3000th numbers after the value 0,
# wrapping around the list as necessary. You need to sum these three numbers and return the result.

def compute_code(numbers):
    # Find the 1000th, 2000th, and 3000th numbers after the value 0, wrapping around the list as necessary
    coord1 = numbers[(numbers.index(0) + 1000) % len(numbers)]
    coord2 = numbers[(numbers.index(0) + 2000) % len(numbers)]
    coord3 = numbers[(numbers.index(0) + 3000) % len(numbers)]
    # Return the sum of the three numbers
    return coord1 + coord2 + coord3


def p(*args):
    #return
    import sys
    print(*args, file=sys.stderr, flush=True)

# Part 1 - n=1 for part 1, n=10 for part 2
def mix(numbers, n=1):
    # Move each number forward or backward in the file a number of positions equal to the value of the number being moved
    # decorate sort undecorate
    decorated = [(i, x) for i,x in enumerate(numbers)]
    initial = decorated[:]  # copy
    p("init   ", [x[1] for x in decorated])
    for round in range(n):
        for i, x in initial:
            curr_i = decorated.index((i, x))
            decorated.remove((i,x))
            new_i = (curr_i + x) % (len(numbers) - 1)
            if new_i:
                decorated.insert(new_i, (i,x))
            else:
                decorated.append((i,x))
        p(f"round={round}", [x[1] for x in decorated])

    return [x for i,x in decorated]



# Test the function with the given encrypted file
def test(n=1, data_list= [1, 2, -3, 3, -2, 0, 4], result_list=[1, 2, -3, 4, 0, 3, -2], result=3, key=811589):
    encrypted_file = data_list
    encrypted_file = mix(encrypted_file, n)
    result = compute_code(encrypted_file)
    expected_result = result
    expected_list = result_list
    # Check that the result is correct
    if result == expected_result:
        print("Result is correct")
    else:
        print("Result is incorrect. \n"
              "Expected:", expected_result,
              "/n  Actual:", result)
    # Check that the final state of the list is correct

    if encrypted_file == expected_list:
        print("Final list is correct")
    else:
        print("Final list is incorrect. \n"
              "Expected:", expected_list,
              "\n  Actual:", encrypted_file)

# Part 2
# First, you need to apply the decryption key, 811589153. Multiply each number by the decryption key before you begin;
# this will produce the actual list of numbers to mix.
#
# Second, you need to mix the list of numbers ten times. The order in which the numbers are mixed does not change during mixing;
# the numbers are still moved in the order they appeared in the original, pre-mixed list.
# (So, if -3 appears fourth in the original list of numbers to mix, -3 will be the fourth number to move during each round of mixing.)
#
# Using the same example as above:
# Test Part 2

def apply_key(numbers, key=811589153):
    return [x * key for x in numbers]



def read_input_file(filename="20input.txt"):
    with open(filename, "r") as myfile:
        data = myfile.read()
    return map(int, data.split())



if __name__ == "__main__":
    print("Part 1")
    test()
    print("Part 2")
    data_list = apply_key([1, 2, -3, 3, -2, 0, 4], key=811589153)
    test(n=10, data_list=data_list, result_list=[0, -2434767459, 1623178306, 3246356612, -1623178306, 2434767459, 811589153],
         result=1623178306)

    # data = list(read_input_file())
    # res = compute_code(mix(apply_key(data), 10))
    # print(res)
