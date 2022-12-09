# I've had it with Haskell

head_pos = (0,0)
tail_pos = (0,0)

with open("input.txt") as f:
    def parseLine(line):
        [direction, count] = line.split(" ")
        return (direction, int(count))
    instructions = [parseLine(line) for line in f.readlines()]

def distance(a, b):
    (ax, ay) = a
    (bx, by) = b
    dx = abs(ax-bx)
    dy = abs(ay-by)
    return max(dx, dy)

def euclidean_distance(a, b):
    (ax, ay) = a
    (bx, by) = b
    dx = abs(ax-bx)
    dy = abs(ay-by)
    return dx*dx+dy*dy

def update_tail():
    global head_pos
    global tail_pos
    possible_steps = [(x, y) for x in range(tail_pos[0]-1, tail_pos[0]+1+1) for y in range(tail_pos[1]-1, tail_pos[1]+1+1)]
    best_step = min(possible_steps, key=lambda p:euclidean_distance(p, head_pos))
    if distance(tail_pos, head_pos) > 1:
        tail_pos = best_step

tail_positions = set()
tail_positions.add((0,0))

def step(direction):
    global head_pos
    global tail_pos

    

    step_offsets = {
        'U':(0, 1),
        'D':(0, -1),
        'L':(-1, 0),
        'R':(1, 0)
    }
    step_offset = step_offsets[direction]
    head_pos = (head_pos[0] + step_offset[0], head_pos[1] + step_offset[1])
    update_tail()
    tail_positions.add(tail_pos)

for instruction in instructions:
    (direction, count) = instruction
    for _ in range(count):
        step(direction)
        print(head_pos, tail_pos)
print(len(tail_positions))