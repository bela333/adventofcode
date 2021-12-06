#Based on concepts I found on the subreddit
import numpy as np

with open("input.txt") as f:
    numbers = [int(a) for a in f.readline().strip().split(",")]
    freq = [0]*9
    for n in numbers:
        freq[n] += 1
    freq = np.array(freq)
    #Matrix: 
    #0 1 0 0 0 0 0 0 0
    #0 0 1 0 0 0 0 0 0
    #0 0 0 1 0 0 0 0 0
    #0 0 0 0 1 0 0 0 0
    #0 0 0 0 0 1 0 0 0
    #0 0 0 0 0 0 1 0 0
    #1 0 0 0 0 0 0 1 0
    #0 0 0 0 0 0 0 0 1
    #1 0 0 0 0 0 0 0 0
    m = np.identity(8)
    m = np.vstack([m, np.zeros(8)])
    m = np.hstack((np.array([0, 0, 0, 0, 0, 0, 1, 0, 1]).reshape((9, 1)),m))
    #Apply 256 steps
    m = np.linalg.matrix_power(m, 256)
    result = (m @ freq)
    result = result.sum()
    print(result)