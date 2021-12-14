from typing import Counter

def add(dict, key, val):
    if key not in dict:
        dict[key] = 0
    dict[key] += val

def round(pairs, rules):
    p = pairs.copy()
    for r in rules:
        [pattern, insert] = r
        if pattern in pairs:
            count = pairs[pattern]
            add(p, pattern, -count)
            add(p, pattern[0]+insert, count)
            add(p, insert+pattern[1], count)
    return p

with open("input.txt") as f:
    state = f.readline().strip()
    f.readline()
    rules = [l.strip().split(" -> ") for l in f.readlines()]
    i = 0
    pairs = {}
    while i < len(state)-1:
        pair = state[i:i+2]
        add(pairs, pair, 1)
        i += 1
    for _ in range(40):
        pairs = round(pairs, rules)
    c = Counter()
    for p in pairs:
        c.update({p[0]: pairs[p]})
        c.update({p[1]: pairs[p]})
    c = dict(c)
    #Fix duplicates
    c[state[0]] -= 1
    c[state[-1]] -= 1
    c = {k: v//2 for k, v in c.items()}
    c[state[0]] += 1
    c[state[-1]] += 1
    c = Counter(c)
    freq = c.most_common()
    print(freq[0][1]-freq[-1][1])