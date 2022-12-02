total=0
with open("input.txt") as f:
    for line in f:
        [opponent, you_result] = line.split()
        if you_result == 'X':
            #Lose
            you = chr((ord(opponent)-ord('A')-1)%3+ord('X'))
        elif you_result == 'Y':
            #draw
            you = chr(ord(opponent)-ord('A')+ord('X'))
        else:
            #win
            you = chr((ord(opponent)-ord('A')+1)%3+ord('X'))
        #print(you)
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

