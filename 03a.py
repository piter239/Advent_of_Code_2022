with open('03input.txt','r') as f:
    res = []
    for line in f:
        half = len(line)//2
        for c in line[:half]:
            if c in line[half:]:
                res += [c]
                break
    print(sum(map(lambda c:ord(c) - ord('a') + 1 if c.islower() else ord(c) - ord('A') + 27, res)))
