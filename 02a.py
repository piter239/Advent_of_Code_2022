your = {"X":1, "Y":2, "Z":3}

# (he - you) % 3
i_he = "ABC"
i_you = "XYZ"
out = {0:3, 1:0, 2:6}

with open('02input.txt','r') as f:
    res = 0
    for line in f:
        he, you = line.split()
        res += your[you] + out[(i_he.index(he) - i_you.index(you)) % 3]

    print(res)
