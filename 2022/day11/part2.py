from __future__ import annotations
from typing import List

# https://stackoverflow.com/a/312464
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

class Monkey:
    def __init__(self, items: List[int], operation: str, increase: int | str, divisibility: int, if_true: int, if_false: int):
        self.all_div = 0
        self.items = items
        self.operation = operation
        self.increase = increase
        self.divisibility = divisibility
        self.if_true = if_true
        self.if_false = if_false
        self.inspections = 0
    def __repr__(self) -> str:
        return '"' + ", ".join([str(a) for a in self.items]) + '"'
    def handle_round(self, monkeys: List[Monkey]):
        for item in self.items:
            self.pass_item(item, monkeys)
        self.items = []
    def pass_item(self, item: int, monkeys: List[Monkey]):
        self.inspections += 1
        val = self.increase
        if isinstance(val, str):
            val = item
        if self.operation == '+':
            item += val
        elif self.operation == '*':
            item *= val
        item = item % self.all_div
        if item % self.divisibility == 0:
            # divisible
            monkeys[self.if_true].items.append(item)
            pass
        else:
            # not divisible
            monkeys[self.if_false].items.append(item)
            pass

def parse_monkey(lines: List[str]) -> Monkey:
    starting_items = [int(a.strip()) for a in lines[1].split(":")[1].split(",")]
    old_index = lines[2].find("old")
    operation = lines[2][old_index+4]

    increase = lines[2][old_index+6:]
    if increase != "old":
        increase = int(increase)
    divisibility = int(lines[3][lines[3].find("by ")+3:])
    if_true = int(lines[4][lines[4].find("monkey ")+7:])
    if_false = int(lines[5][lines[5].find("monkey ")+7:])
    return Monkey(starting_items, operation, increase, divisibility, if_true, if_false)
    


with open("input.txt") as f:
    lines = [l.strip() for l in f.readlines()]
    parts = list(chunks(lines, 7))
    monkeys = [parse_monkey(m) for m in parts]

all_div = 1

for monkey in monkeys:
    # Assuming all divisibility values are prime/pairwise coprime
    all_div *= monkey.divisibility

for monkey in monkeys:
    monkey.all_div = all_div

for i in range(10000):
    for monkey in monkeys:
        monkey.handle_round(monkeys)
inspections = [a.inspections for a in monkeys]
inspections.sort()
[a, b] = inspections[-2:]
print(a*b)