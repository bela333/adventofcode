import matplotlib.pyplot as plt

with open("input.txt") as f:
    print("Calculating...")
    numbers = [int(a) for a in f.readline().strip().split(",")]
    frequency_table = [0]*7
    next = [0]*7
    for n in numbers:
        frequency_table[n] += 1
    vals = [sum(frequency_table)]
    for i in range(256):
        next[(i+2)%len(frequency_table)] = frequency_table[i%len(frequency_table)]
        frequency_table[(i-1)%len(frequency_table)] += next[(i-1)%len(frequency_table)]
        next[(i-1)%len(frequency_table)] = 0
        vals.append(sum(frequency_table) + sum(next))
    print("Plotting...")
    plt.plot(vals)
    plt.show()