def binary_to_number(binary):
    return sum([(1<<(len(binary)-i-1))*a for i, a in enumerate(binary)])

with open("input.txt") as f:
    lines = [line.strip() for line in f]
    frequency = [0]*len(lines[0])
    for line in lines:
        frequency = [a + (b=='1') for a, b in zip(frequency, line)]
    threshold = len(lines)/2
    gamma = [a>threshold for a in frequency]
    epsilon = [not a for a in gamma]
    gamma = binary_to_number(gamma)
    epsilon = binary_to_number(epsilon)
    print(gamma*epsilon)