import re

pattern = re.compile('mul\((\d+),(\d+)\)')

with open("input.txt") as file:
    content = file.read()

matches = pattern.findall(content)

result = 0
for (a,b) in matches:
    subresult = int(a)*int(b)
    result = result+subresult

print(result)