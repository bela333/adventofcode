with open("input.txt") as f:
    pos = [0, 0]
    aim = 0
    for line in f:
        [instruction, value] = line.strip().split(" ")
        value = int(value)
        if instruction == "forward":
            pos[0] += value
            pos[1] += aim*value
        elif instruction == "down":
            aim += value
        elif instruction == "up":
            aim -= value
    print(pos)
    print(pos[0]*pos[1])