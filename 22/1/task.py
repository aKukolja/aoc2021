import re
from collections import defaultdict
from itertools import product


matcher = re.compile("^(on|off) x=(-?\\d+)..(-?\\d+),y=(-?\\d+)..(-?\\d+),z=(-?\\d+)..(-?\\d+)$")


class Cube:

    def __init__(self, value, bounds):
        self._value = value
        xmin, xmax, ymin, ymax, zmin, zmax = bounds
        self._start = xmin, ymin, zmin
        self._stops = xmax, ymax, zmax

    def value(self):
        return self._value

    def is_in(self, coord):
        x, y, z = coord
        xmin, ymin, zmin = self._start
        xmax, ymax, zmax = self._stops
        if xmin <= x <= xmax and ymin <= y <= ymax and zmin <= z <= zmax:
            return True
        return False


class World:

    def __init__(self):
        self._world = []

    def add(self, value, bounds):
        cube = Cube(value, bounds)
        self._world.append(cube)

    def value(self, coord):
        for cube in reversed(self._world):
            if cube.is_in(coord):
                return cube.value()
        return 0


if __name__ == "__main__":
    world = World()
    with open("data.txt", "r") as f:
        for line in f:
            match = matcher.match(line.strip())
            bounds = map(int, match.groups()[1:])
            val = {
                "on": 1,
                "off": 0
            }[match.group(1)]
            world.add(val, bounds)

    count = 0
    xmin, xmax, ymin, ymax, zmin, zmax = -50, 50, -50, 50, -50, 50
    for coord in product(range(xmin, xmax+1), range(ymin, ymax+1), range(zmin, zmax)):
        count += world.value(coord)

    print(count)


    
    



