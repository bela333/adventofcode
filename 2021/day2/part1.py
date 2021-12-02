with open("input.txt") as f:
    x = 0
    y = 0
    instructions = {
        "forward": (1, 0),
        "up": (0, -1),
        "down": (0, 1),
    }
    for line in f:
        [instruction, value] = line.strip().split(" ")
        value = int(value)
        (dx, dy) = instructions[instruction]
        x += dx*value
        y += dy*value
    print(x, y)
    print(x*y)