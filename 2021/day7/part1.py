def sum_distance(pos, positions):
    return sum([abs(a-pos) for a in positions])

with open("input.txt") as f:
    positions = [int(a) for a in f.readline().strip().split(",")]
    min = min(positions)
    max = max(positions)
    p = sum_distance(min, positions)
    j = 0
    for i in range(1, len(positions)):
        d = sum_distance(positions[i], positions)
        if d < p:
            p = d
            j = i
    print(p)