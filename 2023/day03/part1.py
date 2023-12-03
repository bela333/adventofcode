import re

with open("input.txt") as f:
    lines = [l.strip() for l in f]

height = len(lines)
width = len(lines[0])

regex = r"\d+"

def get_neighbours(y, x1, x2):
    for _y in range(y-1, y+2):
        for _x in range(x1-1, x2+1):
            if _y >= 0 and _y < height and _x >= 0 and _x < width:
                if _y == y and _x >= x1 and _x < x2:
                    continue
                yield (_x, _y)
    
sum = 0

for y, line in enumerate(lines):
    for m in re.finditer(regex, line):
        actual_part = False
        span = m.span()
        part_number = int(m.group())
        for (nx, ny) in get_neighbours(y, *span):
            if lines[ny][nx] != '.' and not (ord('0')<=ord(lines[ny][nx])<=ord('9')):
                actual_part=True
        if actual_part:
            print(part_number)
            sum += part_number

print(sum)