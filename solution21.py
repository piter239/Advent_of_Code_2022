import re

def monkey_math(input_str):
    # Use a regular expression to replace each job with a function definition
    # that calls the functions and returns the result of the job
    def_str = re.sub(r"(\w+): (\w+) (\W+) (\w+)", r"def \1(): return \2() \3 \4()", input_str)
    # Use a regular expression to replace each number with a function definition
    # that returns the number
    def_str = re.sub(r"(\w+): (\d+)", r"def \1(): return \2", def_str)
    # Execute the function definitions
    d = {}
    exec(def_str, d)
    # Call the root function and return the result
    return int(eval("root()", d))

# Test the function
input_small = """
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
"""

def read_jobs(filename):
    with open(filename) as f:
        return f.read()

def test_monkey_math():
    input_str = read_jobs("21input.txt")
    # Ensure that the correct result is produced for the given input
    assert monkey_math(input_small) == 152
    print(monkey_math(input_str))

if __name__  == "__main__":
    test_monkey_math()
