from __future__ import annotations
from typing import List, Tuple, Generator
import heapq



class Field:
    def __init__(self, lines: List[str]):
        self.start = (0,0)
        self.end = (0,0)
        y = 0
        for l in lines:
            if 'S' in l:
                x = l.index('S')
                self.start = (x,y)
                lines[y] = l.replace('S', 'a')
                l = lines[y]
            if 'E' in l:
                x = l.index('E')
                self.end = (x,y)
                lines[y] = l.replace('E', 'z')
            y += 1

        self.lines = [[ord(a)-ord('a') for a in l] for l in lines]
    
    def __repr__(self) -> str:
        header = "Start: {} {}\nEnd: {} {}\n".format(self.start[0], self.start[1], self.end[0], self.end[1])
        return header + "\n".join(["".join([chr(a+ord('a')) for a in l]) for l in self.lines])
    

    def pathfind(self, from_coords: Tuple[int, int], to_coords: Tuple[int, int]) -> int | None:
        visited = set()
        q: List[Tuple[int, int, int]] = []
        heapq.heappush(q, (0, from_coords[0], from_coords[1]))
        visited.add(from_coords)
        while len(q) > 0:
            (d,x, y) = heapq.heappop(q)
            
            if (x,y) == to_coords:
                return d
            for n in self.neighbours(x, y):
                if n not in visited:
                    visited.add(n)
                    heapq.heappush(q, (d+1, n[0], n[1]))
        return None

        
        

    def neighbours(self, x, y) -> List[Tuple[int, int]]:

        n = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

        o = []
        for (nx, ny) in n:
            if nx < 0 or ny < 0 or ny >= len(self.lines) or nx >= len(self.lines[0]):
                continue
            if not (self.lines[ny][nx] <= self.lines[y][x]+1):
                continue
            o.append((nx, ny))
        
        return o

with open("input.txt") as f:
    field = Field([a.strip() for a in f.readlines()])


print(field.pathfind(field.start, field.end))