import statistics
start = ['(', '[', "{", '<']
end = [')', ']', "}", '>']

cost = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

class Unexpected(Exception):
    def __init__(self, character,*args: object) -> None:
        self.expected = character
        super().__init__("Unexpected character: {}".format(character))

class Incomplete(Exception):
    def __init__(self, stack, *args: object) -> None:
        self.stack = stack
        super().__init__(*args)

def parse_line(line):
    stack = []
    for c in line:
        if c in start:
            stack.append(end[start.index(c)])
        else:
            expected = stack.pop()
            if c != expected:
                raise Unexpected(c)
    if len(stack) > 0:
        raise Incomplete(stack)


with open("input.txt") as f:
    scores = []
    for line in f:
        try:
            parse_line(line.strip())
        except Unexpected as err:
            pass
        except Incomplete as err:
            score = 0
            for c in reversed(err.stack):
                score *= 5
                score += cost[c]
            scores.append(score)
    print(statistics.median(scores))