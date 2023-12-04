sum = 0

with open("input.txt") as f:
    for l in f:
        l = l.strip()
        _, p = l.split(": ")
        winning, current = p.split(" | ")
        current = [int(a) for a in map(str.strip, current.split(" ")) if len(a) > 0]
        winning = [int(a) for a in map(str.strip, winning.split(" ")) if len(a) > 0]
        s = 0
        for c in current:
            if c in winning:
                s += 1
        if s > 0:
            sum += 2**(s-1)

print(sum)