nums = [
    (1, "one"),
    (2, "two"),
    (3, "three"),
    (4, "four"),
    (5, "five"),
    (6, "six"),
    (7, "seven"),
    (8, "eight"),
    (9, "nine"),
]

def first(s: str):
    for i in range(len(s)):
        sub = s[:i+1]
        for (num, label) in nums:
            if len(sub) >= len(label) and sub[-len(label):] == label:
                return num
        if ord('0')<=ord(sub[-1])<=ord('9'):
            return int(sub[-1])

def last(s: str):
    for i in range(len(s)):
        sub = s[-(i+1):]
        for (num, label) in nums:
            if len(sub) >= len(label) and sub[:len(label)] == label:
                return num
        if ord('0')<=ord(sub[0])<=ord('9'):
            return int(sub[0])

sum=0

with open("input.txt") as f:
    for l in f:
        l = l.strip()
        n = int(str(first(l))+str(last(l)))
        sum += n

print(sum)