with open('01input.txt','r') as f:
    max_sum = -1

    c_sum = 0
    for line in f:
        if line != '\n':
            c_sum += int(line.strip())
        else:
            if max_sum < c_sum:
                max_sum = c_sum
            c_sum = 0

    print(max_sum)
