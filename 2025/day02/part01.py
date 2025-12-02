with open("input.txt") as f:
    content = f.read()


def garbage(n: int):
    s = str(n)
    l = len(s)
    if l % 2 != 0:
        return False
    s1 = s[: l // 2]
    s2 = s[l // 2 :]
    return s1 == s2


content = [elem.split("-") for elem in content.strip().split(",")]
c = 0
for r in content:
    a = int(r[0])
    b = int(r[1])
    for i in range(a, b + 1):
        if garbage(i):
            print(i)
            c += i

print(c)
