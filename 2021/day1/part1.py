with open("input.txt") as f:
    c = 0
    nums = [int(a.strip()) for a in f]
    for i in range(1, len(nums)):
        if(nums[i] > nums[i-1]):
            c += 1
    print(c)