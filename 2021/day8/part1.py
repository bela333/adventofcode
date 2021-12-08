class Entry:
    def __init__(self, line):
        [p1, p2] = line.split("|")
        p1 = p1.strip()
        p2= p2.strip()
        self.patterns = p1.split(" ")
        self.outputs = p2.split(" ")
    
    def __repr__(self):
        return " ".join(self.patterns) + " | " + " ".join(self.outputs)

    def one_four_seven_eight(self):
        return sum([len(a) in [2, 4, 3, 7] for a in self.outputs])
    
    

with open("input.txt") as f:
    entries = [Entry(line) for line in f]
    print(sum([a.one_four_seven_eight() for a in entries]))