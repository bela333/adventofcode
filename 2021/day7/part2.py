def distance_to_fuel(distance):
    return (distance*(distance+1))//2

def sum_distance(pos, positions):
    return sum([distance_to_fuel(abs(a-pos)) for a in positions])

with open("input.txt") as f:
    positions = [int(a) for a in f.readline().strip().split(",")]
    min = min(positions)
    max = max(positions)
    p = sum_distance(min, positions)
    j = min
    for i in range(min, max):
        d = sum_distance(i, positions)
        if d < p:
            p = d
            j = i
    print(p)