def garbage(n: int, m: int):
    s = str(n)
    l = len(s)
    if l % m != 0:
        return False
    l = l // m
    base = s[0:l]
    for i in range(l, len(s), l):
        c = s[i : i + l]
        if c != base:
            return False
    return True


if __name__ == "__main__":
    with open("input.txt") as f:
        content = f.read()

    content = [elem.split("-") for elem in content.strip().split(",")]
    found = set()
    for r in content:
        a = int(r[0])
        b = int(r[1])
        for m in range(2, len(r[1]) + 1):
            for i in range(a, b + 1):
                if garbage(i, m):
                    found.add(i)

    print(sum(found))
