from typing import List

with open("input.txt") as f:
    lines = f.readlines()

_state = {'x':1, 'cycle_count':1}

def handle_noop(args: List[str], state, before_cycle, after_cycle):
    before_cycle(state)
    after_cycle(state)

def handle_addx(args: List[str], state, before_cycle, after_cycle):
    before_cycle(state)
    after_cycle(state)
    before_cycle(state)
    state['x'] += int(args[0])
    after_cycle(state)

commands = {
    'noop': handle_noop,
    'addx': handle_addx
}

output = ""

screen_x = 0
screen_y = 0

for line in lines:
    parts = line.strip().split(" ")
    def before_cycle(state):
        global strengths
        global screen_x
        global screen_y
        global output

        #cycle_count = state['cycle_count']
        registerX = state['x']
        if abs(registerX-screen_x) <= 1:
            output += "█"
        else:
            output += " "
        
    def after_cycle(state):
        global screen_x
        global screen_y
        
        state['cycle_count'] += 1
        screen_x += 1
        if screen_x >= 40:
            screen_x = 0
            screen_y += 1
    
    commands[parts[0]](parts[1:], _state, before_cycle, after_cycle)

for i in range(len(output)):
    if (i % 40) == 0:
        print()
    print(output[i], end="")
print()