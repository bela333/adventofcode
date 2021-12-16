from bitarray import bitarray
from bitarray.util import ba2int

su = 0
class Packet:
    def __init__(self, version):
        global su
        self.version = version
        su += version
    def __repr__(self) -> str:
        return "Version: " + str(self.version) + ". "
class LiteralPacket(Packet):
    def __init__(self, version, lit):
        super().__init__(version)
        self.lit = lit
    def __repr__(self) -> str:
        return super().__repr__() + "Literal: {}. ".format(self.lit)
    
class OperatorPacket(Packet):
    def __init__(self, version, packets):
        super().__init__(version)
        self.packets = packets
    def __repr__(self) -> str:
        ps = "\n".join(["\n".join([" - " + l for l in str(p).splitlines()]) for p in self.packets])
        return super().__repr__() + "\n" + ps

def parse_number(bits):
    running = True
    out = bitarray()
    while running:
        out += bits[1:5]
        running = bits[0] == 1
        bits = bits[5:]
    return ba2int(out), bits

def parse_packet_list(bits: bitarray):
    packets = []
    while len(bits) > 0:
        p, bits = parse_packet(bits)
        packets.append(p)
    return packets
def parse_packet_count(bits: bitarray, count):
    packets = []
    for _ in range(count):
        p, bits = parse_packet(bits)
        packets.append(p)
    return packets, bits

def parse_packet(bits: bitarray):
    version = ba2int(bits[:3])
    type = ba2int(bits[3:6])
    bits = bits[6:]
    if type == 4:
        lit, bits = parse_number(bits)
        p = LiteralPacket(version, lit)
        return p, bits
    else:
        type = bits[0]
        if type == 0:
            #length based
            length = ba2int(bits[1:16])
            p = parse_packet_list(bits[16:16+length])
            bits = bits[16+length:]
            return OperatorPacket(version, p), bits
        else:
            #count based
            length = ba2int(bits[1:12])
            p, bits = parse_packet_count(bits[12:], length)
            return OperatorPacket(version, p), bits

with open("input.txt") as f:
    l = f.readline().strip()
    #b = bitarray(len(l))
    #for i, v in enumerate(l):
    #    b[i] = int(v)
    b = bitarray()
    b.frombytes(bytes.fromhex(l))
    packet, b = parse_packet(b)
    print(packet)
    print(su)