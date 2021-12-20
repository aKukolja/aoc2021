import re
import numpy as np
from math import pi, sin, cos
from itertools import product, permutations
from collections import defaultdict
import time


matcher = re.compile("^--- scanner (\\d+) ---$")


class Bidirectional:

    def __init__(self):
        self._left = dict()
        self._right = dict()

    def add(self, key, val):
        self._left[key] = val
        self._right[val] = key
        assert(len(self._left) == len(self._right))

    def get_from_left(self, key):
        return self._left.get(key)

    def get_from_right(self, val):
        return self._right.get(val)

    def left_as_set(self):
        return set(self._left.keys())

    def right_as_set(self):
        return set(self._right.keys())


class Scanner:

    @staticmethod
    def _transform(beacon, t):
        x, y, z = beacon
        return {
                0 : lambda:  (  x,  y,  z ),
                1 : lambda:  (  x, -y, -z ),
                2 : lambda:  (  x,  z, -y ),
                3 : lambda:  (  x, -z,  y ),
                4 : lambda:  (  y,  x, -z ),
                5 : lambda:  (  y, -x,  z ),
                6 : lambda:  (  y,  z,  x ),
                7 : lambda:  (  y, -z, -x ),
                8 : lambda:  (  z,  x,  y ),
                9 : lambda:  (  z, -x, -y ),
                10: lambda:  (  z,  y, -x ),
                11: lambda:  (  z, -y,  x ),
                12: lambda:  ( -x,  y, -z ),
                13: lambda:  ( -x, -y,  z ),
                14: lambda:  ( -x,  z,  y ),
                15: lambda:  ( -x, -z, -y ),
                16: lambda:  ( -y,  x,  z ),
                17: lambda:  ( -y, -x, -z ),
                18: lambda:  ( -y,  z, -x ),
                19: lambda:  ( -y, -z,  x ),
                20: lambda:  ( -z,  x, -y ),
                21: lambda:  ( -z, -x,  y ),
                22: lambda:  ( -z,  y,  x ),
                23: lambda:  ( -z, -y, -x )
        }[t]()

    def __init__(self, scanner_id, beacons):
        self._id = scanner_id
        self._original = {bid: b for bid, b in enumerate(beacons)}
        self._all = None
        self._expand()

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

    def __str__(self):
        return str(self._id) + " -> " + " | ".join(map(str, self._original))

    @staticmethod
    def _beacon_diff(a, b):
        ax, ay, az = a
        bx, by, bz = b
        return ax - bx, ay - by, az - bz

    @staticmethod
    def _beacon_add(a, b):
        ax, ay, az = a
        bx, by, bz = b
        return ax + bx, ay + by, az + bz

    def _calc_diffs(self, t):
        " difference from each point in cloud to each other point "
        diffs = defaultdict(lambda: Bidirectional())
        for a, b in permutations(self._all[t].items(), 2):
            " TODO: keep in mind duplicate diffs "
            _, a_pos = a
            _, b_pos = b
            diffs[a].add(Scanner._beacon_diff(a_pos, b_pos), b)
            " diffs[b].add(Scanner._beacon_diff(b_pos, a_pos), a) "
        self._diffs[t] = diffs

    def _calc_rots(self, t):
        new_beacons = dict()
        for bid, v in self._original.items():
            new_v = Scanner._transform(v, t)
            new_beacons[bid] = new_v
        self._all[t] = new_beacons

    def _expand(self):
        self._all = dict()
        self._diffs = dict()
        for t in range(24):
            self._calc_rots(t)
            self._calc_diffs(t)

        assert(len(self._diffs) == 24)
        assert(len(self._all) == 24)
        alll = list(self._all.keys())
        assert(all(set(self._all[a].values())!=set(self._all[b].values()) for a, b in permutations(self._all.keys(), 2)))
        
    def _my_point_to_his(my_point, his_point, his_diffs):
        retset = set()
        " this vector points from our reference system to their zero "
        point_diff = Scanner._beacon_diffs(my_point, his_point)
        retset = set(map(lambda x: Scanner._beacon_add(my_point, x), his_diffs))
        return retset

    def match(self, my_tt, candidate):
        " candidate: Scanner "
        my_distances = self._diffs[my_tt]
        for his_tt in range(24):
            his_distances = candidate._diffs[his_tt]
            for (my_point, my_diffs), (his_point, his_diffs) in zip(my_distances.items(), his_distances.items()):
                matching = my_diffs.left_as_set().intersection(his_diffs.left_as_set())
                """
                print(my_diffs.left_as_set())
                print()
                print()
                print(his_diffs.left_as_set())
                """
                if len(matching) >= 12:
                    " this point is contained in both clouds "
                    " calculate their distances "
                    return his_tt, my_point, his_point
        return None


if __name__ == "__main__":
    setup = time.time()
    scanners = []
    with open("test.txt", "r") as f:
        while True:
            scanner = Scanner.from_stream(f)
            if scanner is None:
                break
            scanners.append(scanner)

    zero = scanners[0]
    world = {(zero._id, bid): pos for bid, pos in zero._all[0].items()}
    matched = [(0, zero)]
    others = scanners[1:]

    print("setup", time.time() - setup)

    while len(others) > 0:
        to_remove = None
        for scanner in others:
            for (tt, found), candidate in product(matched, others):
                result = found.match(tt, candidate)
                if result is None:
                    continue
                his_tt, my_pont, his_point = result
                to_remove = his_tt, scanner

                " tt is aligned to world "
                " find my_point in world "
                my_wid = found._id, my_point[0]
                my_world_point = world[my_wid]
                for his_bi_diff in candidate._diffs[his_tt][his_point]:
                    for dist_diff in his_bi_diff.left_as_set():
                        point_id, _ = his_bi_diff.get_from_right(dist_diff)
                        world[(candidate._id, point_id)] = Scanner._beacon_add(my_point[1], dist_diff)
                world[(candidate._id, his_point[0])] = my_point[1]
                
        assert(to_remove is not None)
        t, scanner = to_remove
        others.remove(scanner)
        matched.append((t, scanner))

            


