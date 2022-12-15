def split_by(line: str, by: str):
    i = line.index(by)
    return (line[:i], line[i+len(by):])

def distance(a, b) -> int:
    (ax, ay) = a
    (bx, by) = b
    return abs(ax-bx)+abs(ay-by)


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

y = 2000000
p = set()
for (s, _, d) in sensors:
    sx, sy = s
    dy = abs(sy-y)
    fromx = sx-d+dy
    tox   = sx+d-dy
    for x in range(fromx, tox+1):
        p.add((x, y))
for (_, (bx, by), _) in sensors:
    if by == y and (bx, by) in p:
        p.remove((bx, by))
print(len(p))