repeats = {}

with open("input.txt") as f:
    i = 0
    for l in f:
        l = l.strip()
        _, p = l.split(": ")
        winning, current = p.split(" | ")
        current = [int(a) for a in map(str.strip, current.split(" ")) if len(a) > 0]
        winning = [int(a) for a in map(str.strip, winning.split(" ")) if len(a) > 0]
        matching = 0
        for c in current:
            if c in winning:
                matching += 1
        

        if i in repeats:
            our_repeats = repeats[i]
        else:
            our_repeats = 0
        

        for j in range(i+1, i+1+matching):
            if not (j in repeats):
                repeats[j] = 0
            repeats[j] = repeats[j]+our_repeats+1
        
        i += 1

res = sum(repeats.values())+i
print(res)