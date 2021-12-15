import bisect

nodes = {}
queue = []

with open("input.txt") as f:
    board = [[int(num) for num in line.strip()] for line in f]
height = len(board)*5
width = len(board[0])*5

def get_node(x, y):
    c = (x, y)
    if c not in nodes:
        w = (width//5)
        h = (height//5)
        offset = x // w + y // h
        val = (board[y%h][x%w] + offset - 1)%9+1
        nodes[c] = Node(x, y, val)
        queue.append(nodes[c])
    return nodes[c]

class Node:
    def __init__(self, x, y, weight):
        self.x = x
        self.y = y
        self.weight = weight
        self.total = -1
        self.final = False
    
    def neighbours(self):
        ns = [(-1, 0), (1, 0), (0,-1),(0,1) ]
        for x, y in ns:
            _x = self.x + x
            _y = self.y + y
            if _x >= 0 and _y >= 0 and _x < width and _y < height:
                yield (_x, _y)
    def w(self):
        return self.total + abs(width-1-self.x) + abs(height-1-self.y)
    
    def __lt__(self, rhs):
        return self.w() < rhs.w()
    def __gt__(self, rhs):
        return self.w() > rhs.w()
    def __le__(self, rhs):
        return self.w() <= rhs.w()
    def __ge__(self, rhs):
        return self.w() >= rhs.w()
    def __eq__(self, rhs):
        return self.w() == rhs.w()



start_node = get_node(0, 0)
start_node.total = 0
queue = [start_node]
while len(queue) > 0:
    node = queue.pop(0)
    if node.x == width-1 and node.y == height-1:
        print(node.total)
        break
    for n in node.neighbours():
        n = get_node(n[0], n[1])
        new_weight = n.weight+node.total
        if new_weight < n.total or n.total == -1:
            n.total = new_weight
    queue.sort()