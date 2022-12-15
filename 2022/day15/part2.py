from collections import Counter

def split_by(line: str, by: str):
    i = line.index(by)
    return (line[:i], line[i+len(by):])

def distance(a, b) -> int:
    (ax, ay) = a
    (bx, by) = b
    return abs(ax-bx)+abs(ay-by)

def is_covered(sensors, a) -> bool:
    for (s, _, d) in sensors:
        if distance(s, a) <= d:
            return True
    return False


minx = None
maxx = None

def parse_line(line: str):
    line = split_by(line, "x=")[1]
    (ax, line) = split_by(line, ", ")
    line = split_by(line, "y=")[1]
    (ay, line) = split_by(line, ":")
    line = split_by(line, "x=")[1]
    (bx, line) = split_by(line, ", ")
    line = split_by(line, "y=")[1]
    by = line
    ax, ay, bx, by = int(ax), int(ay), int(bx), int(by)
    a = (ax, ay)
    b = (bx, by)
    return (a, b, distance(a, b))



with open("input.txt") as f:
    sensors = [parse_line(l) for l in f.readlines()]

#spacesize = 20
spacesize = 4000000

possible = Counter()
i = 0
for ((sx, sy), _, d) in sensors:
    i += 1
    print(i/len(sensors))
    d = d + 1
    for dy in range(-d, d+1):
        y = sy+dy
        if y < 0 or y > spacesize:
            continue
        x1 = sx-d+dy
        x2 = sx+d-dy
        if x1 >= 0 and x1 <= spacesize:
            possible.update({(x1, y): 1})
        if x2 >= 0 and x2 <= spacesize:
            possible.update({(x2, y): 1})
        
print(len(possible))
possible_ = []
i = 0
for (a, v) in possible.items():
    i += 1
    if v < 2:
        continue
    if i % 100 == 0:
        print(i, i/len(possible))
    if not is_covered(sensors, a):
        (x, y) = a
        print(a)
        print(x*4000000+y)
        break
