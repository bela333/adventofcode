#TODO
import re
import math

with open("input.txt") as f:
    l = f.readline().strip()
(x1, x2, y1, y2) = re.compile("target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)").match(l).groups()
x1, x2, y1, y2 = int(x1), int(x2), int(y1), int(y2)

#(2Vx-n+1)*n
#2Vx*n-n*n+n
#Vx*n=x
#(x+(n*n+n)/2)/n
def calc_vx(x, n):
    return (x+(n*n+n)/2)/n
def count_integers(a, b):
    if a > b:
        return count_integers(b, a)
    if math.floor(b)-math.floor(a) == 0:
        return 0
    frac, _ = math.modf(b)
    if frac == 0:
        return math.floor(b)-math.floor(a)-1
    return math.floor(b)-math.floor(a)
def find_count_for_line(y):
    best_y_vel = (-y)-1
    steps = (best_y_vel*2)+2

    min, max = calc_vx(x1, steps), calc_vx(x2, steps)
    return count_integers(min, max)

for i in range(y1, y2+1):
    print(i)
    print(find_count_for_line(i))
#find_count_for_line(-10)