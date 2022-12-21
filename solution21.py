import re
from sympy import symbols, Eq, solve, simplify


def monkey_math(input_str):
    # Use a regular expression to replace each job with a function definition
    # that calls the functions and returns the result of the job
    def_str = re.sub(r"(\w+): (\w+) (\W) (\w+)", r"def \1(): return \2() \3 \4()", input_str)
    # Use a regular expression to replace each number with a function definition
    # that returns the number
    def_str = re.sub(r"(\w+): (\d+)", r"def \1(): return \2", def_str)
    # Execute the function definitions
    d = {}
    print(def_str)
    exec(def_str, d)
    # Call the root function and return the result
    return eval("root()", d)


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


print(monkey_math(input_small))

# ___ Part 2 ________

simply_def = """
def simply(input_str):
    if 'x' in input_str:
        return input_str
    return int(eval(input_str))
"""


def monkey_eq(input_str):
    #
    def_str = re.sub(r"(\w+): (\w+) (\W) (\w+)", r"def \1(): return simply('(' + str(\2()) + '\3' +  str(\4()) + ')')",
                     input_str)
    # Use a regular expression to replace each number with a function definition
    # that returns the number
    def_str = re.sub(r"(\w+): (\d+)", r"def \1(): return '\2'", def_str)
    # explicitly state humn() = x
    def_str += "\ndef humn(): return 'x'"
    # add simply function
    def_str += simply_def
    # Execute the function definitions
    d = {}
    exec(def_str, d)
    # Call the root function and return the result
    res = eval("root()", d)
    return res


# Test the function
input_small = """
root: pppw = sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
"""


def test_monkey_math2():
    # Ensure that the correct result is produced for the test input
    res_small = monkey_eq(input_small)

    # print(res_small)

    # Define the variable
    x = symbols('x')

    # Convert the equation into SymPy's format

    lhs, rhs = res_small[1:-1].split('=')
    print(lhs, rhs)

    eq = Eq(eval(lhs), eval(rhs))

    # Solve the equation
    solution = solve(eq, x)
    # Print the solution
    print(f"Solution of small eq {solution}, should be equal to 301")
    assert solution == [301]

    input_str = read_jobs("21input.txt")

    res = monkey_eq(input_str)
    print(res)

    # Convert the equation into SymPy's format
    x = symbols('x')
    lhs1, rhs1 = res[1:-1].split('=')

    eq1 = Eq(eval(lhs1), eval(rhs1))

    # Solve the equation
    solution1 = solve(eq1, x)
    # Print the solution
    print(f"Solution of full equation {solution1}")
    result = eq1.subs({x: solution1[0]})
    print()
    print(f"Result of full equation {result}")

    print(simplify(lhs1), '=', simplify(rhs1))

if __name__ == "__main__":
    test_monkey_math2()
