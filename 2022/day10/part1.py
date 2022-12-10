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

strengths = 0

for line in lines:
    parts = line.strip().split(" ")
    def before_cycle(state):
        global strengths
        cycle_count = state['cycle_count']
        registerX = state['x']
        if (cycle_count)%40 == 20:
            signal = registerX*cycle_count
            strengths += signal
    def after_cycle(state):
        state['cycle_count'] += 1
    
    commands[parts[0]](parts[1:], _state, before_cycle, after_cycle)
print(strengths)