your = {"A":1, "B":2, "C":3}

# (he - you) % 3
i_he = "ABC"
d_you = {"X":2, "Y":0, "Z":1}
out = {"Y":3, "X":0, "Z":6}

with open('02input.txt','r') as f:
    res = 0
    for line in f:
        he, outcome = line.split()
        res += your[i_he[(i_he.index(he) + d_you[outcome]) % 3]] + out[outcome]

    print(res)
