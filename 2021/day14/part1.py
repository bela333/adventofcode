from typing import Counter


with open("input.txt") as f:
    state = f.readline().strip()
    f.readline()
    rules = [l.strip().split(" -> ") for l in f.readlines()]
    for _ in range(10):
        i = 0
        while i < len(state)-1:
            part = state[i:i+2]
            for rule in rules:
                [pattern, insert] = rule
                if part == pattern:
                    state = state[:i+1] + insert + state[i+1:]
                    i += 1
                    break
            i += 1
    counter = Counter(state)
    freq = counter.most_common()
    print(freq[0][1]-freq[-1][1])