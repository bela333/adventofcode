class Field:
    def __init__(self) -> None:
        self.field = {}
        self.min = None
        self.max = None
    
    def update_bounds(self, coords):
        if self.min is None or self.max is None:
            self.min = coords
            self.max = coords
            return
        self.min = (min(self.min[0], coords[0]), min(self.min[1], coords[1]))
        self.max = (max(self.max[0], coords[0]), max(self.max[1], coords[1]))
    
    def put_wall(self, coords):
        self.field[coords] = "#"
        self.update_bounds(coords)
    
    def simulate_sand(self, coords):
        (x, y) = coords
        alive = True
        
        while alive:
            if y > self.max[1]:
                return True
            if not self.is_blocked((x, y+1)): # Not blocked below?
                y += 1
            elif not self.is_blocked((x-1, y+1)): # Not blocked to the left?
                y += 1
                x -= 1
            elif not self.is_blocked((x+1, y+1)): # Not blocked to the right?
                y += 1
                x += 1
            else:
                alive = False # Could not move anywhere
        self.put_sand((x, y))
        return False

    
    def put_sand(self, coords):
        self.field[coords] = "+"
    
    def is_blocked(self, coords) -> bool:
        return coords in self.field
    
    def draw_rectangle(self, fromcoords, tocoords):
        (fromx, fromy) = fromcoords
        (tox, toy) = tocoords
        fromx,tox = min(fromx, tox), max(fromx, tox)
        fromy,toy = min(fromy, toy), max(fromy, toy)
        for x in range(fromx, tox+1):
            for y in range(fromy, toy+1):
                self.put_wall((x, y))
    def draw_line(self, line):
        for i in range(len(line)-1):
            fromcoords = line[i]
            tocoords = line[i+1]
            self.draw_rectangle(fromcoords, tocoords)

            

def parse_line(line):
    return [tuple(map(int, a.split(","))) for a in line.split(" -> ")]

with open("input.txt") as f:
    data = [parse_line(a) for a in f.readlines()]

field = Field()

for line in data:
    field.draw_line(line)

i = 0
while( not field.simulate_sand((500, 0))):
    i += 1
print(i)
