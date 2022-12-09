# I've had it with Haskell
from typing import List, Tuple
knot_positions: List[Tuple[int, int]] = [(0, 0)]*10

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

def update_tails():
    global knot_positions
    for i in range(len(knot_positions)-1):
        i = len(knot_positions)-i-2
        tail_pos = knot_positions[i]
        head_pos = knot_positions[i+1]
        possible_steps = [(x, y) for x in range(tail_pos[0]-1, tail_pos[0]+1+1) for y in range(tail_pos[1]-1, tail_pos[1]+1+1)]
        best_step = min(possible_steps, key=lambda p:euclidean_distance(p, head_pos))
        if distance(tail_pos, head_pos) > 1:
            tail_pos = best_step
        knot_positions[i] = tail_pos

tail_positions = set()
tail_positions.add((0,0))

def step(direction):
    global knot_positions

    

    step_offsets = {
        'U':(0, 1),
        'D':(0, -1),
        'L':(-1, 0),
        'R':(1, 0)
    }
    step_offset = step_offsets[direction]
    head_pos = knot_positions[-1]
    head_pos = (head_pos[0] + step_offset[0], head_pos[1] + step_offset[1])
    knot_positions[-1] = head_pos
    update_tails()
    tail_positions.add(knot_positions[0])

for instruction in instructions:
    (direction, count) = instruction
    for _ in range(count):
        step(direction)
        print(knot_positions)
print(len(tail_positions))