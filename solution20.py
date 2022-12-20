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
    return
    import sys
    print(*args, file=sys.stderr, flush=True)

def mix(numbers):
    # Move each number forward or backward in the file a number of positions equal to the value of the number being moved
    # decorate sort undecorate
    decorated = [(i, x) for i,x in enumerate(numbers)]
    p("init", decorated)
    for i, x in decorated.copy():
        curr_i = decorated.index((i, x))
        decorated.remove((i,x))
        new_i = (curr_i + x) % (len(numbers) - 1)
        if new_i:
            decorated.insert(new_i, x)
        else:
            decorated.append(x)
        p(f"i={i}, x={x}, (curr_i+x)%(len(numbers)-1)={(curr_i + x) % (len(numbers))}, curr_i={curr_i}, new_i={new_i}", decorated)

    return decorated



# Test the function with the given encrypted file
encrypted_file = [1, 2, -3, 3, -2, 0, 4]
encrypted_file = mix(encrypted_file)
result = compute_code(encrypted_file)
expected_result = 3
expected_list = [1, 2, -3, 4, 0, 3, -2]
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


def read_input_file(filename="20input.txt"):
    with open(filename, "r") as myfile:
        data = myfile.read()
    return map(int, data.split())


data = list(read_input_file())
print(len(list(data)), len(set(data)))
res = compute_code(mix(data))
print(res)
