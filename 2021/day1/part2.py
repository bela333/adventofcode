def window(a, size):
    for i in range(len(a)-size+1):
        yield a[i:i+size]

with open("input.txt") as f:
    c = 0
    nums = [int(a.strip()) for a in f]
    nums = [sum(a) for a in window(nums, 3)]
    for i in range(1, len(nums)):
        if(nums[i] > nums[i-1]):
            c += 1
    print(c)