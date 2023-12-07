from typing import Union, List

class Range:
    def __init__(self, f: int, t: int, c: int) -> None:
        self.f=f
        self.t=t
        self.c=c
    def translate(self, n: int) -> Union[int, None]:
        if n >= self.f and n < self.f+self.c:
            return n-self.f+self.t
        return None

seed_to_soil = []
soil_to_fertilizer = []
fertilizer_to_water = []
water_to_light = []
light_to_temperature = []
temperature_to_humidity = []
humidity_to_location = []

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
            currentmap.append(Range(bid, aid, count))
            
def resolve(map: List[Range], n: int) -> int:
    for m in map:
        v = m.translate(n)
        if v is not None:
            return v
    return n

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
        a = resolve(m, a)
    return a

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

print(min([get_whole_chain(a) for a in required_seeds]))