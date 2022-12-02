# Disclaimer: I don't remember writing this code
total=0
with open("input.txt") as f:
    for line in f:
        [opponent, you] = line.split()
        score = 0
        if(ord(opponent)-ord('A') == ord(you)-ord('X')):
            #draw
            score += 3
        elif(
            (opponent == "A" and you == "Y") or
            (opponent == "B" and you == "Z") or
            (opponent == "C" and you == "X")
            ):
            #You win
            score += 6
            pass
        else:
            #You lose
            score += 0
            pass
        score += ord(you)-ord('X')+1
        total += score
print(total)

