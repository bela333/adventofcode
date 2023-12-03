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
    
gears = {}

def add_gear(x, y, n):
    if (x, y) not in gears:
        gears[(x, y)] = []
    gears[(x, y)].append(n)

for y, line in enumerate(lines):
    for m in re.finditer(regex, line):
        span = m.span()
        part_number = int(m.group())
        for (nx, ny) in get_neighbours(y, *span):
            if lines[ny][nx] == '*':
                add_gear(nx, ny, part_number)

sum = 0

for (x, y) in gears:
    gear_numbers = gears[(x, y)]
    if len(gear_numbers) == 2:
        sum += gear_numbers[0]*gear_numbers[1]
print(sum)