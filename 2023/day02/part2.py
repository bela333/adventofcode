def process_pull(s: str, vals):
    for cubes in s.split(", "):
        count, kind = cubes.split(" ")
        count = int(count)
        if kind == "red":
            if vals[0] <= 0:
                vals[0] = count
            vals[0] = max(vals[0], count)
        elif kind == "green":
            if vals[1] <= 0:
                vals[1] = count
            vals[1] = max(vals[1], count)
        elif kind == "blue":
            if vals[2] <= 0:
                vals[2] = count
            vals[2] = max(vals[2], count)

sum = 0

with open("input.txt") as f:
    for l in f:
        l = l.strip()
        game_name, pulls = l.split(": ")
        _, game_id = game_name.split(" ")
        game_id = int(game_id)
        pulls = map(str.strip, pulls.split(";"))
        vals = [0, 0, 0]
        for a in pulls:
            process_pull(a, vals)
        sum += vals[0]*vals[1]*vals[2]

print(sum)