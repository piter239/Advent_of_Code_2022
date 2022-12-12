with open('03input.txt','r') as f:
    res = []
    trio = []
    for line in f:
        if len(trio) < 2:
            trio += [line]
        else:
            for c in line:
                if c in trio[0] and c in trio[1]:
                    res += [c]
                    break
            trio = []
    print(sum(map(lambda c:ord(c) - ord('a') + 1 if c.islower() else ord(c) - ord('A') + 27, res)))
