start = ['(', '[', "{", '<']
end = [')', ']', "}", '>']

cost = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

class Unexpected(Exception):
    def __init__(self, character,*args: object) -> None:
        self.expected = character
        super().__init__("Unexpected character: {}".format(character))

def parse_line(line):
    stack = []
    for c in line:
        if c in start:
            stack.append(end[start.index(c)])
        else:
            expected = stack.pop()
            if c != expected:
                raise Unexpected(c)


with open("input.txt") as f:
    acc = 0
    for line in f:
        try:
            parse_line(line.strip())
        except Unexpected as err:
            print(err)
            acc += cost[err.expected]
    print(acc)