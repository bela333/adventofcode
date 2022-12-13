from typing import Tuple, List

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
    pairs = [(a[0].strip(), a[1].strip()) for a in chunks(f.readlines(), 3)]


pairs = [(parse_expression(a)[0], parse_expression(b)[0]) for (a, b) in pairs]
results = [check_correct(a, b) for (a, b) in pairs]
print(sum([i+1 for (i, b) in enumerate(results) if b]))