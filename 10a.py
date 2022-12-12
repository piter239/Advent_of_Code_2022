# solution to https://adventofcode.com/2022/day/10


timeline = [1, 1]  # during time 0 AND time 1 the value of register x == 1

with open("10input.txt", "r") as f:
    # read each line of the file
    for line in f:
        cmd, *attr = line.split()

        if cmd == 'noop':
            timeline.append(timeline[-1])
        elif cmd == 'addx':
            timeline.append(timeline[-1])
            timeline.append(timeline[-1] + int(attr[0]))
        else:
            print('unexpected input', line)
            quit()

print("Part I", sum(i * timeline[i] for i in range(20, len(timeline), 40)))

width = 40  # pixels in one line
screen_line = ''
for i in range(len(timeline) - 1):
    try:
        if abs(i % width - timeline[i + 1]) <= 1:
            screen_line += '#'
        else:
            screen_line += '.'
        if len(screen_line) == width:
            print(screen_line)
            screen_line = ''
    except:
        print('_' * 40)
