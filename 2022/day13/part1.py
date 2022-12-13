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

# True: left < right
# False: left > right
# None: left == right
def check_correct(left, right) -> bool | None:
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return None
        return left < right
    if isinstance(left, list) and isinstance(right, list):
        for (l, r) in zip(left, right):
            v = check_correct(l, r)
            if v is not None:
                return v
        if len(left) == len(right):
            return None
        return len(left) < len(right)
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