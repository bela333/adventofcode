from typing import Union, List, Self

class Range:
    def __init__(self, i: int, count: int) -> None:
        self.i = i
        self.count = count
    def intersect(self, other: Self) -> Union[Self, None]:
        if other.i >= self.i+self.count:
            return None
        # Innentől a másik kezdeti pontja, a mi végpontunk előtt van
        if self.i >= other.i+other.count:
            return None
        # Innentől a mi kezdőpontunk a másik végpontja előtt van
        f = max(self.i, other.i)
        t = min(self.i+self.count, other.i+other.count)
        return Range(f, t-f)
    def subtract(self, other: Self) -> List[Self]:
        a = Range(self.i, other.i-self.i) # from `self.i` to `other.i-1`
        if a.count <= 0 or a.count > self.count:
            a = None
        b = Range(other.i+other.count, self.i+self.count-other.i+other.count)
        if b.count <= 0 or b.count > self.count:
            b = None
        return [r for r in [a, b] if r is not None]

    def __repr__(self) -> str:
        return "<{}:{}>".format(self.i, self.count)

class Translation:
    def __init__(self, f: int, t: int, c: int) -> None:
        self.f=f
        self.from_range = Range(f, c)
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

def parse_seeds(seeds: List[int]) -> List[Range]:
    o = []
    while len(seeds) >= 2:
        a, b = seeds[:2]
        o.append(Range(a, b))
        seeds = seeds[2:]
    return o


def handle_part(part: List[str]):
    if part[0].startswith("seeds: "):
        global required_seeds
        required_seeds = parse_seeds([int(a) for a in part[0].split(" ")[1:]])
    else:
        currentmap = maps[part[0]]
        part = part[1:]
        for line in part:
            aid, bid, count = map(int, line.split(" "))
            currentmap.append(Translation(bid, aid, count))
            
def resolve(map: List[Translation], ranges: List[Range]) -> List[Range]:
    out_ranges = []
    for range in ranges:
        remaining_ranges = [range]
        for translation in map:
            intersection = range.intersect(translation.from_range)
            if intersection is None:
                continue
            added_range = Range(intersection.i-translation.f+translation.t, intersection.count)
            out_ranges.append(added_range)
            remaining_ranges = [a for r in remaining_ranges for a in r.subtract(added_range)]
        out_ranges.extend(remaining_ranges)
    return out_ranges

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
    print(a)
    for m in ms:
        a = resolve(m, a)
        print(a)
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

get_whole_chain(required_seeds)