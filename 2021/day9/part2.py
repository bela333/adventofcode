import math


class Board:
    def __init__(self, arr):
        self.arr = arr

    def is_low(self, x, y):
        p = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in p:
            _x = x+dx
            _y = y+dy
            if _x < 0 or _y < 0 or _y >= len(self.arr) or _x >= len(self.arr[0]):
                continue
            if self.arr[_y][_x] <= self.arr[y][x]:
                return False
        return True

    def iter(self):
        for y in range(len(self.arr)):
            for x in range(len(self.arr[y])):
                yield x, y

    def find_relative_low(self, x, y):
        p = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        lowest = None
        ox, oy = x, y
        for dx, dy in p:
            _x = x+dx
            _y = y+dy
            if _x < 0 or _y < 0 or _y >= len(self.arr) or _x >= len(self.arr[0]):
                continue
            if self.arr[_y][_x] < self.arr[oy][ox]:
                lowest = self.arr[_y][_x]
                oy = _y
                ox = _x
        if lowest is not None:
            return ox, oy

    def find_flow_up_direction(self, x, y):
        p = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in p:
            _x = x+dx
            _y = y+dy
            if _x < 0 or _y < 0 or _y >= len(self.arr) or _x >= len(self.arr[0]):
                continue
            if self.arr[_y][_x] != 9 and self.find_relative_low(_x, _y) == (x, y):
                yield _x, _y

    def basin_size(self, x, y):
        acc = 1
        for _x, _y in self.find_flow_up_direction(x, y):
            acc += self.basin_size(_x, _y)
        return acc

with open("input.txt") as f:
    board = [[int(n) for n in a.strip()] for a in f]
    board = Board(board)
    sizes = []
    for x, y in board.iter():
        if board.is_low(x, y):
            sizes.append(board.basin_size(x, y))
    sizes.sort()
    sizes.reverse()
    print(math.prod(sizes[:3]))