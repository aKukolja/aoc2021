from itertools import permutations, product
from collections import defaultdict
import time
import re


matcher = re.compile("^--- scanner (\\d+) ---$")


class Scanner:

    @staticmethod
    def from_stream(itt):
        try:
            header = matcher.match(next(itt).strip())
        except StopIteration:
            return None
        if header is None:
            raise Exception()
        beacons = set()
        while True:
            try:
                line = next(itt)
            except StopIteration:
                break
            if line is None:
                break
            stripped = line.strip()
            if stripped == "":
                break
            x, y, z = map(int, map(lambda s: s.strip(), stripped.split(",")))
            beacons.add((x, y, z))
        return Scanner(int(header.group(1)), beacons)

    def __init__(self, my_id, beacons):
        self._position = None
        self._t = None
        self._id = my_id
        self._beacons = dict()
        self._diffs = dict()
        for t in range(24):
            new_beacons = set()
            for b in beacons:
                new_beacons.add(Scanner._transform(b, t))
            self._beacons[t] = new_beacons
        for t in range(24):
            self._diffs[t] = defaultdict(lambda: set())
            for a, b in permutations(self._beacons[t], 2):
                self._diffs[t][a].add(Scanner._b_diff(a, b))

    @staticmethod
    def _transform(beacon, t):
        x, y, z = beacon
        return {
                17 : lambda: (  y,  z,  x ),
                1 : lambda: (  y,  x, -z ),
                2 : lambda: ( -y,  z, -x ),
                3 : lambda: (  z,  y, -x ),
                4 : lambda: (  z,  x,  y ),
                5 : lambda: ( -z,  x, -y ),
                6 : lambda: ( -y,  x,  z ),
                7 : lambda: (  x, -z,  y ),
                8 : lambda: (  x, -y, -z ),
                9 : lambda: ( -z, -x,  y ),
                10: lambda: (  y, -x,  z ),
                11: lambda: (  y, -z, -x ),
                12: lambda: ( -y, -x, -z ),
                13: lambda: ( -x, -y,  z ),
                14: lambda: ( -z, -y, -x ),
                15: lambda: ( -x,  z,  y ),
                16: lambda: ( -x, -z, -y ),
                0: lambda: (  x,  y,  z ),
                18: lambda: (  x,  z, -y ),
                19: lambda: ( -x,  y, -z ),
                20: lambda: (  z, -y,  x ),
                21: lambda: (  z, -x, -y ),
                22: lambda: ( -y, -z,  x ),
                23: lambda: ( -z,  y,  x )
        }[t]()

    @staticmethod
    def _b_diff(a, b):
        ax, ay, az = a
        bx, by, bz = b
        return ax - bx, ay - by, az - bz

    @staticmethod
    def _b_add(a, b):
        ax, ay, az = a
        bx, by, bz = b
        return ax + bx, ay + by, az + bz

    def _determine_position(self, their_position, their_point, my_t, my_point):
        self._t = my_t
        " their position + their point = global position of our point "
        our_global_point = Scanner._b_add(their_position, their_point)
        " our_globa_point - our_point = our_global position "
        self._position = Scanner._b_diff(our_global_point, my_point)

    def set_position(self, t, pos):
        self._t = t
        self._position = pos

    def global_points(self):
        assert(self._t is not None)
        assert(self._position is not None)
        " our_global_position + point_diff = point_global_position "
        return {Scanner._b_add(self._position, b) for b in self._beacons[self._t]}

    def match(self, other):
        assert(self._t is not None)
        assert(self._position is not None)
        my_diffs = self._diffs[self._t]
        for his_t in range(24):
            his_diffs = other._diffs[his_t]
            for (my_point, my_p_diffs), (his_point, his_p_diffs) in product(my_diffs.items(), his_diffs.items()):
                overlap = my_p_diffs.intersection(his_p_diffs)
                if len(overlap) >= 11:
                    other._determine_position(self._position, my_point, his_t, his_point)
                    return other.global_points()
        return None

    def manhattan(self, other):
        return sum(map(abs, Scanner._b_diff(self._position, other._position)))


if __name__ == "__main__":
    start = time.time()
    scanners = []
    with open("data.txt", "r") as f:
        while True:
            scanner = Scanner.from_stream(f)
            if scanner is None:
                break
            scanners.append(scanner)

    zero = scanners[0]
    zero.set_position(0, (0, 0, 0))
    world = {b for b in zero.global_points()}
    found = [zero]
    others = scanners[1:]

    print("setup", time.time() -start)
    
    while len(others) > 0:
        to_remove = None
        for f, nf in product(found, others):
            result = f.match(nf)
            if result is None:
                continue
            to_remove = nf
            world = world.union(result)
            break
        assert(to_remove is not None)
        others.remove(to_remove)
        found.append(to_remove)

    print("manhattan", max(map(lambda x: x[0].manhattan(x[1]), permutations(scanners, 2))))

    print("beacons", len(world))

