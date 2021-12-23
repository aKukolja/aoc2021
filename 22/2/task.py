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

    def volume(self):
        xmin, ymin, zmin = self._start
        xmax, ymax, zmax = self._stops
        x_len = xmax - xmin + 1
        y_len = ymax - ymin + 1
        z_len = zmax - zmin + 1
        return x_len * y_len * z_len

    def intersect(self, other, val):
        a_x_min, a_y_min, a_z_min = self._start
        a_x_max, a_y_max, a_z_max = self._stops

        b_x_min, b_y_min, b_z_min = other._start
        b_x_max, b_y_max, b_z_max = other._stops

        x_min = max(a_x_min, b_x_min)
        x_max = min(a_x_max, b_x_max)
        y_min = max(a_y_min, b_y_min)
        y_max = min(a_y_max, b_y_max)
        z_min = max(a_z_min, b_z_min)
        z_max = min(a_z_max, b_z_max)

        if x_max >= x_min and y_max >= y_min and z_max >= z_min:
            return Cube(val, (x_min, x_max, y_min, y_max, z_min, z_max))
        return None

    def weighted(self):
        return self._value * self.volume()


class World:

    def __init__(self):
        self._world = []

    def add(self, value, bounds):
        cube = Cube(value, bounds)

        if cube.value() == 0:
            to_add = []
            for c in self._world:
                cval = c.value()
                intersection = cube.intersect(c, -cval)
                if intersection is None:
                    continue
                to_add.append(intersection)
            self._world = self._world + to_add
        else:
            to_add = []
            for c in self._world:
                cval = c.value()
                correction = cube.intersect(c, -cval)
                if correction is None:
                    continue
                to_add.append(correction)
            self._world = self._world + to_add
            self._world.append(cube)

    def count(self):
        return sum(c.weighted() for c in self._world)


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

    print(world.count())


    
    



