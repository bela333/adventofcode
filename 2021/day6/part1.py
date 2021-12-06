def step(list):
    added = [8 for a in list if a == 0]
    step = [6 if a == 0 else a-1 for a in list]
    return added + step

with open("input.txt") as f:
    numbers = [int(a) for a in f.readline().strip().split(",")]
    for _ in range(80):
        numbers = step(numbers)
    print(len(numbers))