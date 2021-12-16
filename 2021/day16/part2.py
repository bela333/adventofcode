from bitarray import bitarray
from bitarray.util import ba2int

class Packet:
    def __init__(self, version):
        self.version = version
    def __repr__(self) -> str:
        return self.name + "V" + str(self.version) + ". "
    def eval(self):
        raise NotImplemented()
class LiteralPacket(Packet):
    def __init__(self, version, lit):
        super().__init__(version)
        self.lit = lit
        self.name = "Lit"
    def __repr__(self) -> str:
        return super().__repr__() + "Literal: {}. ".format(self.lit)
    def eval(self):
        return self.lit
    
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

class SumPacket(OperatorPacket):
    def __init__(self, version, packets):
        super().__init__(version, packets)
        self.name = "Sum"
    def eval(self):
        acc = 0
        for p in self.packets:
            acc += p.eval()
        return acc

class ProductPacket(OperatorPacket):
    def __init__(self, version, packets):
        super().__init__(version, packets)
        self.name = "Prod"
    def eval(self):
        acc = 1
        for p in self.packets:
            acc *= p.eval()
        return acc
class MinPacket(OperatorPacket):
    def __init__(self, version, packets):
        super().__init__(version, packets)
        self.name = "Min"
    def eval(self):
        return min([p.eval() for p in self.packets])
class MaxPacket(OperatorPacket):
    def __init__(self, version, packets):
        super().__init__(version, packets)
        self.name = "Max"
    def eval(self):
        return max([p.eval() for p in self.packets])
class GtPacket(OperatorPacket):
    def __init__(self, version, packets):
        super().__init__(version, packets)
        self.name = "Gt"
    def eval(self):
        return 1 if self.packets[0].eval() > self.packets[1].eval() else 0
class LtPacket(OperatorPacket):
    def __init__(self, version, packets):
        super().__init__(version, packets)
        self.name = "Lt"
    def eval(self):
        return 1 if self.packets[0].eval() < self.packets[1].eval() else 0
class EqPacket(OperatorPacket):
    def __init__(self, version, packets):
        super().__init__(version, packets)
        self.name = "Eq"
    def eval(self):
        return 1 if self.packets[0].eval() == self.packets[1].eval() else 0

operators = {
    0: SumPacket,
    1: ProductPacket,
    2: MinPacket,
    3: MaxPacket,
    5: GtPacket,
    6: LtPacket,
    7: EqPacket
}

def parse_packet(bits: bitarray):
    version = ba2int(bits[:3])
    ptype = ba2int(bits[3:6])
    bits = bits[6:]
    if ptype == 4:
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
            return operators[ptype](version, p), bits
        else:
            #count based
            length = ba2int(bits[1:12])
            p, bits = parse_packet_count(bits[12:], length)
            return operators[ptype](version, p), bits

with open("input.txt") as f:
    l = f.readline().strip()
    #b = bitarray(len(l))
    #for i, v in enumerate(l):
    #    b[i] = int(v)
    b = bitarray()
    b.frombytes(bytes.fromhex(l))
    packet, b = parse_packet(b)
    print(packet)
    print(packet.eval())