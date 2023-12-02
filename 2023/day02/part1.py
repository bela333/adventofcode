def process_pull(s: str):
    r,g,b=0,0,0
    for cubes in s.split(", "):
        count, kind = cubes.split(" ")
        count = int(count)
        if kind == "red":
            r += count
        elif kind == "green":
            g += count
        elif kind == "blue":
            b += count
    if r > 12 or g > 13 or b > 14:
        return False
    return True

sum = 0

with open("input.txt") as f:
    for l in f:
        l = l.strip()
        game_name, pulls = l.split(": ")
        _, game_id = game_name.split(" ")
        game_id = int(game_id)
        pulls = map(str.strip, pulls.split(";"))
        if all(process_pull(a) for a in pulls):
            sum += game_id

print(sum)