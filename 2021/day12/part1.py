nodes = {}

def _add(to, what):
    if to not in nodes:
        nodes[to] = []
    nodes[to].append(what)

def add(a, b):
    _add(a, b)
    _add(b, a)

def filter_small(path, next):
    return [a for a in next if not a.islower() or a not in path]

def find_paths(path, end):
    if path[-1] == end:
        return [path]
    paths = []
    for next in filter_small(path, nodes[path[-1]]):
        paths.extend(find_paths(path + [next], end))
    return paths

with open("input.txt") as f:
    for l in f:
        [a, b] = l.strip().split("-")
        add(a, b)
    print(len(find_paths(["start"], "end")))