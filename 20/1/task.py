from collections import defaultdict
from itertools import product


class Image:

    def __init__(self, algo):
        self._algo = algo
        self._raster = defaultdict(lambda: 0)
        assert(len(algo) == 512)
        self._minx, self._maxx = 0, -1
        self._miny, self._maxy = 0, -1

    def add_row(self, row):
        for i, v in enumerate(row):
            self._raster[(i, self._maxy+1)] = v
        self._maxy += 1
        self._maxx = max(self._maxx, len(row)-1)

    @staticmethod
    def _kernel(coord):
        x, y = coord
        return [
            (x-1, y-1), (x, y-1), (x+1, y-1),
            (x-1, y), (x, y), (x+1, y),
            (x-1, y+1), (x, y+1), (x+1, y+1)
        ]

    @staticmethod
    def _to_index(bits):
        return sum(v * 2**i for i, v in enumerate(reversed(bits)))

    def _expand_pixel(self, coord):
        kernel = Image._kernel(coord)
        bits = [self._raster[kcoord] for kcoord in kernel]
        algo_index = Image._to_index(bits)
        return self._algo[algo_index]


    def expand(self):
        for_outer = self._expand_pixel((self._minx-2, self._miny-2))
        new_raster = defaultdict(lambda: for_outer)
        for coord in product(range(self._minx-1, self._maxx+2), range(self._miny-1, self._maxy+2)):
            new_raster[coord] = self._expand_pixel(coord)
        self._raster = new_raster
        self._minx -= 1
        self._maxx += 1
        self._miny -= 1
        self._maxy += 1

    def lit(self):
        return sum(self._raster.values())

    def __str__(self):
        retval = str(self._minx) + ", " + str(self._maxx) + "\n"
        retval += str(self._miny) + ", " + str(self._maxy) + "\n  "
        for x in range(self._minx-5, self._maxx+6):
            retval += " " if x not in range(10) else str(x)
        retval += "\n"
        for y in range(self._miny-5, self._maxy+6):
            retval += "  " if y not in range(10) else (str(y) + " ")
            for x in range(self._minx-5, self._maxx+6):
                retval += "#" if self._raster[(x, y)] == 1 else "."
            retval += "\n"
        return retval


if __name__ == "__main__":
    img = None
    with open("data.txt", "r") as f:
        for line in f:
            stripped = line.strip()
            if img is None:
                img = Image([0 if c == '.' else 1 for c in stripped])
            else:
                if stripped == "":
                    continue
                img.add_row([0 if c == '.' else 1 for c in stripped])
    print(img)
    print()
    img.expand()
    print(img)
    print()
    img.expand()
    print(img)
    print()
    print(img.lit())

