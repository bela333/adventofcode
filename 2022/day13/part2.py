from typing import Tuple, List
from functools import total_ordering

# https://stackoverflow.com/a/312464
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def parse_number(input: str) -> Tuple[int, str]:
    i = 0
    while input[i].isdigit():
        i += 1
    num = int(input[:i], 10)
    rest = input[i:]
    return (num, rest)

def parse_brackets(input: str) -> Tuple[List, str]:
    assert input[0] == '['
    if input[1] == ']':
        return ([], input[2:])
    input = ',' + input[1:]
    l = []
    while input[0] != "]":
        assert input[0] == ','
        (val, input) = parse_expression(input[1:])
        l.append(val)
    input = input[1:]
    return (l, input)



def parse_expression(input: str) -> Tuple[List | int, str]:
    if input[0] == '[':
        return parse_brackets(input)
    else:
        return parse_number(input)

def check_correct(left, right) -> bool | None:
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return None
        return left < right
    if isinstance(left, list) and isinstance(right, list):
        if len(left) == 0 and len(right) == 0:
            return None
        if len(left) == 0 and len(right) != 0:
            return True
        if len(right) == 0 and len(left) != 0:
            return False
        v = check_correct(left[0], right[0])
        if v is None:
            return check_correct(left[1:], right[1:])
        else:
            return v
    if isinstance(left, int):
        return check_correct([left], right)
    if isinstance(right,int):
        return check_correct(left, [right])
    return None
        

with open("input.txt") as f:
    lines = [parse_expression(l.strip())[0] for l in f.readlines() if l.strip() != ""]

@total_ordering
class Value:
    def __init__(self, val) -> None:
        self.val = val
    
    def __lt__(self, other):
        return check_correct(self.val, other.val)
    def __eq__(self, other) -> bool:
        return check_correct(self.val, other.val) is None

lines.append([[2]])
lines.append([[6]])

lines = [Value(l) for l in lines]
lines.sort()
lines = [l.val for l in lines]

print(lines)

two = 0
six = 0
for i in range(len(lines)):
    if lines[i] == [[2]]:
        two = i
    if lines[i] == [[6]]:
        six = i
print((two+1)*(six+1))