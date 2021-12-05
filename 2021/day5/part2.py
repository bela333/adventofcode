import re

line_re = re.compile('(\d+),(\d+) -> (\d+),(\d+)')

def combine_bounds(a, b):
    ((ax1, ay1), (ax2, ay2)) = a
    ((bx1, by1), (bx2, by2)) = b
    return ((min(ax1, bx1), min(ay1, by1)), (max(ax2, bx2), max(ay2, by2)))

def lines_bounds(lines):
    r = lines[0].bounds()
    for l in lines:
        r = combine_bounds(r, l.bounds())
    return r

class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    def from_string(line):
        l = line_re.match(line)
        x1 = int(l.group(1))
        y1 = int(l.group(2))
        x2 = int(l.group(3))
        y2 = int(l.group(4))
        return Line(x1, y1, x2, y2)
    def aa(self):
        return self.x1 == self.x2 or self.y1 == self.y2
    def iter(self):
        b = self.bounds()
        if self.aa():
            for x in range(b[0][0], b[1][0]+1):
                for y in range(b[0][1], b[1][1]+1):
                    yield (x, y)
        else:
            for x in range(b[0][0], b[1][0]+1):
                #Trust me, it works
                y = (self.y1*(self.x2-x)-self.y2*(self.x1-x))//(self.x2-self.x1)
                yield (x, y)
    def __repr__(self) -> str:
        return "({},{} -> {},{})".format(self.x1, self.y1, self.x2, self.y2)
    def bounds(self):
        return ((min(self.x1, self.x2), min(self.y1, self.y2)), (max(self.x1, self.x2), max(self.y1, self.y2)))

class Board:
    def __init__(self, bounds) -> None:
        self.bounds = bounds
        self.width = bounds[1][0] - bounds[0][0]+1
        self.height = bounds[1][1] - bounds[0][1]+1
        self.board = [[0]*self.width for _ in range(self.height)]
    def plot(self, point):
        (x, y) = point
        self.board[y-self.bounds[0][1]][x-self.bounds[0][0]] += 1
    def plot_line(self, line):
        for point in line.iter():
            self.plot(point)
    def __repr__(self) -> str:
        return "\n".join([str(row) for row in self.board])
    def count_intersections(self):
        return sum([sum([point>1 for point in row]) for row in self.board])

with open("input.txt") as f:
    lines = [Line.from_string(a.strip()) for a in f]
    bounds = lines_bounds(lines)
    b = Board(bounds)
    for l in lines:
        b.plot_line(l)
    print(b.count_intersections())