with open('01input.txt','r') as f:

    max_sums = [0, 0, 0, 0]

    c_sum = 0
    for line in f:
        if line != '\n':
            c_sum += int(line.strip())
        else:
            max_sums[3], c_sum = c_sum, 0
            i = 3
            while 0 < i and max_sums[i] > max_sums[i-1]:
                max_sums[i-1], max_sums[i] = max_sums[i], max_sums[i-1]
                i -= 1

            c_sum = 0

    print(sum(max_sums[:3]))
    print(max_sums)
