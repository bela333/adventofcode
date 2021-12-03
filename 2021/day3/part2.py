def binary_to_number(binary):
    return sum([(1<<(len(binary)-i-1))*a for i, a in enumerate(binary)])

def bit_criteria(lines, index):
    ones = sum([a[index] for a in lines])
    threshold = len(lines)/2
    value = not ones<threshold
    return value

def find_value(lines, epsilon):
    index = 0
    while len(lines) > 1:
        value = bit_criteria(lines, index)
        value = not value if epsilon else value
        lines = [a for a in lines if a[index] == value]
        index += 1
    return lines[0]

with open("input.txt") as f:
    lines = [line.strip() for line in f]
    lines = [[a == '1' for a in line] for line in lines]
    gamma = find_value(lines, False)
    print(gamma)
    epsilon = find_value(lines, True)
    print(epsilon)
    gamma = binary_to_number(gamma)
    epsilon = binary_to_number(epsilon)
    print(gamma*epsilon)