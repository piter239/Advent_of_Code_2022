test = '''1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122'''

digits = {'0': 0, '1': 1, '2': 2, '-': -1, '=': -2}
rdigits = {v: k for k, v in digits.items()}

def str2int(s):
    res = 0
    for c in s:
        res = res * 5 + digits[c]
    return res

def int2str(n):
    res = []
    while n > 0:
        res += [(n % 5)] # reversed order
        n //= 5
    check_carry = True
    while check_carry:
        check_carry = False
        i = 0
        while i < len(res):
            if res[i] > 2:
                if i + 1 >= len(res):
                    res += [0]
                res[i + 1] += 1
                res[i] -= 5
                check_carry = True
            i += 1
    while res[-1] == 0:
        res.pop()   # remove trailing zeros
    return ''.join(map(rdigits.get, reversed(res)))

# test str2int and int2str after each other on the test string
def test_str2int_int2str():
    for s in test.splitlines():
        assert int2str(str2int(s)) == s

if __name__ == '__main__':
    # for s in test.splitlines():
    #     r = str2int(s)
    #     print(s, r , int2str(r), int2str(r) == s)
    test_str2int_int2str()

    with open('25input.txt') as f:
        s = sum(map(str2int, f.read().splitlines()))
    print(int2str(s))
