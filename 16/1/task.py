from itertools import chain


class Operator:

    def sum_versions(self):
        s = self.version
        for c in self._children:
            s += c.sum_versions()
        return s

    def __init__(self, p_ver, p_type):
        self.version = p_ver
        self.type = p_type
        self._children = []

    def consume(self, bits, start):
        consumed = 0
        length_id = int(bits[start+consumed:start+consumed+1], 2)
        # print("length id", length_id, "at", start+consumed)
        consumed += 1

        if length_id == 0:
            sub_packet_bit_count = int(bits[start+consumed:start+consumed+15], 2)
            consumed += 15
            sub_consumed = 0
            while sub_consumed < sub_packet_bit_count:
                p_consumed, packet = get_packet(bits, start+consumed)
                sub_consumed += p_consumed
                consumed += p_consumed
                self._children.append(packet)
            assert(sub_consumed == sub_packet_bit_count)

        else:
            sub_packet_count = int(bits[start+consumed:start+consumed+11], 2)
            consumed += 11
            sub_gathered = 0
            while sub_gathered < sub_packet_count:
                p_consumed, packet = get_packet(bits, start+consumed)
                consumed += p_consumed
                self._children.append(packet)
                sub_gathered += 1
            assert(sub_gathered == sub_packet_count)
        
        return consumed


class Literal:

    def sum_versions(self):
        return self.version

    def __init__(self, p_ver, p_type):
        self.version = p_ver
        self.type = p_type
        self.value = None

    def consume(self, bits, start):
        consumed = 0
        val_chain = chain()
        while True:
            segment_header = int(bits[start+consumed:start+consumed+1], 2)
            consumed += 1
            segment = bits[start+consumed:start+consumed+4]
            consumed += 4
            val_chain = chain(val_chain, segment)
            if segment_header == 0:
                break
        self.value = int("".join(val_chain), 2)
        return consumed


def get_header(bits, start):
    consumed = 0
    p_version = int(bits[start:start+3], 2)
    consumed += 3
    p_type = int(bits[start+consumed:start+consumed+3], 2)
    consumed += 3
    # print("header:", p_version, p_type,"at", start, start+consumed)
    return consumed, p_version, p_type

def get_packet(bits, start):
    h_consumed, v, t = get_header(bits, start)
    if t == 4:
        # print("Literal")
        packet = Literal(v, t)
    else:
        # print("Operator")
        packet = Operator(v, t)
    p_consumed = packet.consume(bits, start+h_consumed)
    return h_consumed + p_consumed, packet


def read_bits(name):
    bits = ""
    with open(name, "r") as f:
        for line in f:
            data = line.strip()
            for s in data:
                val = bin(int(s, 16))[2:].zfill(4)
                bits += val
            break
    return bits



if __name__ == "__main__":
    bits = read_bits("literal.txt")
    consumed, packet = get_packet(bits, 0)
    assert(isinstance(packet, Literal))
    assert(consumed == 21)

    bits = read_bits("operator_l0.txt")
    consumed, packet = get_packet(bits, 0)
    assert(isinstance(packet, Operator))
    for v, c in zip([10, 20], packet._children):
        assert(c.value == v)
    assert(consumed == 49)

    bits = read_bits("operator_l1.txt")
    consumed, packet = get_packet(bits, 0)
    assert(isinstance(packet, Operator))
    for v, c in zip([1, 2, 3], packet._children):
        assert(isinstance(c, Literal))
        assert(c.value == v)
    assert(consumed == 51)


    bits = read_bits("data.txt")
    consumed, packet = get_packet(bits, 0)
    assert(consumed <= len(bits))

    print("sum", packet.sum_versions())

    

