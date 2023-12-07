from typing import List

seed_to_soil = {}
soil_to_fertilizer = {}
fertilizer_to_water = {}
water_to_light = {}
light_to_temperature = {}
temperature_to_humidity = {}
humidity_to_location = {}

maps = {
    "seed-to-soil map:": seed_to_soil,
    "soil-to-fertilizer map:": soil_to_fertilizer,
    "fertilizer-to-water map:": fertilizer_to_water,
    "water-to-light map:": water_to_light,
    "light-to-temperature map:": light_to_temperature,
    "temperature-to-humidity map:": temperature_to_humidity,
    "humidity-to-location map:": humidity_to_location
}

def handle_part(part: List[str]):
    if part[0].startswith("seeds: "):
        global required_seeds
        required_seeds = [int(a) for a in part[0].split(" ")[1:]]
    else:
        currentmap = maps[part[0]]
        part = part[1:]
        for line in part:
            aid, bid, count = map(int, line.split(" "))
            for i, j in zip(range(aid, aid+count), range(bid, bid+count)):
                currentmap[j] = i
            


with open("input.txt") as f:
    lines = f.readlines()
    part = []
    for l in lines:
        l = l.strip()
        if l == "":
            handle_part(part)
            part.clear()
        else:
            part.append(l.strip())
    handle_part(part)

def get_map_connection(currentmap, a):
    if a in currentmap:
        return currentmap[a]
    return a

def get_whole_chain(a):
    ms = [
        seed_to_soil,
        soil_to_fertilizer,
        fertilizer_to_water,
        water_to_light,
        light_to_temperature,
        temperature_to_humidity,
        humidity_to_location
    ]
    for m in ms:
        a = get_map_connection(m, a)
    return a

print(min([get_whole_chain(a) for a in required_seeds]))