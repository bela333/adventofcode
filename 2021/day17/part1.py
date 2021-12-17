import re

with open("input.txt") as f:
    l = f.readline().strip()
(x1, x2, y1, y2) = re.compile("target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)").match(l).groups()
x1, x2, y1, y2 = int(x1), int(x2), int(y1), int(y2)
best_y_vel = (-y1)-1
y = 0
for v in range(best_y_vel):
    y += best_y_vel-v

print(y)