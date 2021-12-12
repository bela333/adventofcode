from typing import Counter


nodes = {}

def _add(to, what):
    if to not in nodes:
        nodes[to] = []
    nodes[to].append(what)

def add(a, b):
    _add(a, b)
    _add(b, a)

def can_visit_twice(path, node):
    c = Counter([a for a in path if a.islower()])
    return all([a < 2 for _, a in c.items()]) or node not in path

def filter_small(path, next):
    return [a for a in next if (not a.islower() or can_visit_twice(path, a)) and a != path[0]]

def find_paths(path, end):
    if path[-1] == end:
        return [path]
    paths = []
    filtered = filter_small(path, nodes[path[-1]])
    for next in filtered:
        paths.extend(find_paths(path + [next], end))
    return paths

with open("input.txt") as f:
    for l in f:
        [a, b] = l.strip().split("-")
        add(a, b)
    print(len(find_paths(["start"], "end")))