sum = 0

with open("input.txt") as f:
    for line in f:
        line = line.strip()
        line = list(filter(lambda a: ord('0')<=ord(a)<=ord('9'), line))
        n = str(line[0]) + str(line[-1])
        n = int(n)
        sum += n
print(sum)