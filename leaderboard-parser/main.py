import json
import matplotlib.pyplot as plt
import datetime

def extract_completions(member):
    name = member["name"]
    completions = member["completion_day_level"]
    out = []
    for dayIndex in completions:
        day = completions[dayIndex]
        for partIndex in day:
            part = day[partIndex]
            out.append((name, (int(dayIndex), int(partIndex)), part["get_star_ts"]))
    return out

with open("input.txt", "r") as f:
    data = json.loads(f.read())
finishes = [comp for member in data["members"].values() for comp in extract_completions(member)]
finishes.sort(key=lambda f:f[2])

current_day = max([f[1][0] for f in finishes])
member_count = len(data["members"])

challenge_scores = {}
for day in range(1, current_day+1):
    challenge_scores[(day, 1)] = member_count
    challenge_scores[(day, 2)] = member_count

member_scores = {}
historical_scores = []

# set default member_scores
for _member in data["members"].values():
    name = _member["name"]
    member_scores[name] = 0

for (name, part, time) in finishes:
    current_score = member_scores[name]
    member_scores[name] = current_score + challenge_scores[part]
    challenge_scores[part] = challenge_scores[part]-1
    historical_scores.append((member_scores.copy(), time))

#Normalize scores
#min_time = min(historical_scores, key=lambda f:f[1])[1]
#max_time = max(historical_scores, key=lambda f:f[1])[1]
#historical_scores = [ (scores, time, (time-min_time)/(max_time-min_time)) for (scores, time) in historical_scores]
historical_scores = [ (scores, datetime.datetime.fromtimestamp(time)) for (scores, time) in historical_scores]

fig, ax = plt.subplots()
for member in (member["name"] for member in data["members"].values()):
    x = [time for (_, time) in historical_scores]
    y = [data[member] for (data, _) in historical_scores]
    ax.plot(x, y, label=member)

box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

leg = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()