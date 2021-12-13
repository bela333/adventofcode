import numpy as np

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]
    coords = []
    #parse coordinates
    for l in lines:
        if l == '':
            break
        [x, y] = l.split(",")
        coords.append((int(x), int(y)))
    width = max([x for x, y in coords])+1
    height = max([y for x, y in coords])+1
    field = np.full((height, width), False, bool)
    for x, y in coords:
        field[y, x] = True
    #apply mirrors
    for i in range(lines.index('')+1, len(lines)):
        l = lines[i]
        num = int(l[13:])
        if l[11] == 'y':
            a = np.flip(field[num+1:,:], 0)
            field = field[:num,:]
            field = field | a
        else:
            a = np.flip(field[:,num+1:], 1)
            field = field[:,:num]
            field = field | a
    print("\n".join(["".join(['#' if b else ' ' for b in a]) for a in field]))