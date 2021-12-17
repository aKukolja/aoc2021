import re
from math import floor, sqrt, inf
from itertools import product

class Probe:

    def __init__(self, minx, maxx, miny, maxy):
        self._minx, self._maxx = minx, maxx
        self._miny, self._maxy = miny, maxy

    def find_height(self):
        all_speeds = set()
        record = -inf
        for x_vel, y_vel in product(
                range(floor(sqrt(self._minx*2)), self._maxx+1), 
                range(self._miny, -self._miny)
        ):
            initial = x_vel, y_vel
            x, y = 0, 0
            best_in_run = 0
            while True:
                best_in_run = max(best_in_run, y)
                if x > self._maxx or y < self._miny:
                    break
                if self._minx <= x <= self._maxx and self._miny <= y <= self._maxy:
                    record = max(record, best_in_run)
                    all_speeds.add(initial)
                    break
                x += x_vel
                y += y_vel
                if x_vel > 0:
                    x_vel -= 1
                elif x_vel < 0:
                    x_vel += 1
                y_vel -= 1
        return record, all_speeds


if __name__ == "__main__":
    probe = None
    rr = re.compile("^target area: x=(-?\\d+)\.\.(-?\\d+), y=(-?\\d+)\.\.(-?\\d+)$")
    with open("data.txt", "r") as f:
        for line in f:
            m = rr.match(line.strip())
            probe = Probe(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)))
            break
    highest, speeds = probe.find_height()
    print("highest", highest)
    print("speeds", len(speeds))
