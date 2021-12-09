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


with open("input.txt") as f:
    board = [[int(n) for n in a.strip()] for a in f]
    board = Board(board)
    acc = 0
    for x, y in board.iter():
        if board.is_low(x, y):
            acc += board.arr[y][x]+1
    print(acc)