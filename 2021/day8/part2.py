valid_patterns = ["abcefg","cf","acdeg","acdfg","bcdf","abdfg","abdefg","acf","abcdefg","abcdfg"]


def pattern_to_numbers(pattern):
    return [ord(a)-ord('a') for a in pattern]

valid_patterns = [sorted(pattern_to_numbers(a)) for a in valid_patterns]

def is_pattern_valid(pattern):
    return pattern in valid_patterns

def apply_switch(pattern, swboard):
    return sorted([swboard[a] for a in pattern])

class Entry:
    def __init__(self, line):
        [p1, p2] = line.split("|")
        p1 = p1.strip()
        p2= p2.strip()
        self.patterns = [pattern_to_numbers(a) for a in p1.split(" ")]
        self.outputs = [pattern_to_numbers(a) for a in p2.split(" ")]
    
    def __repr__(self):
        return " ".join(self.patterns) + " | " + " ".join(self.outputs)
    def is_valid(self, swboard):
        for pattern in self.patterns:
            new_pattern = apply_switch(pattern, swboard)
            if not is_pattern_valid(new_pattern):
                return False
        return True
    def find_swboard(self):
        for perm in itertools.permutations(range(7)):
            if self.is_valid(perm):
                return perm
    def get_output(self, swboard):
        o = ""
        for pattern in self.outputs:
            pattern = apply_switch(pattern, swboard)
            n = valid_patterns.index(pattern)
            o += str(n)
        return int(o)

import itertools

with open("input.txt") as f:
    entries = [Entry(line) for line in f]
    acc = 0
    for entry in entries:
        swboard = entry.find_swboard()
        o = entry.get_output(swboard)
        print(o)
        acc += o
    print(acc)