import re

line_re = re.compile("^(\\d+),(\\d+) -> (\\d+),(\\d+)$")


class Thermal:

    def __init__(self, x1, y1, x2, y2):
        self._start = x1, y1
        self._stop = x2, y2
        self._current = self._start
        x_dir = self._stop[0] - self._start[0]
        y_dir = self._stop[1] - self._start[1]
        self._check = abs(x_dir)+1 if x_dir != 0 else abs(y_dir) +1
        if x_dir > 0:
            x_dir = 1
        elif x_dir < 0:
            x_dir = -1
        if y_dir > 0:
            y_dir = 1
        elif y_dir < 0:
            y_dir = -1
        if x_dir != 0 and y_dir != 0:
            print(x1, y1, x2, y2)
            print(x_dir, y_dir)
            raise Exception
        self._going = x_dir, y_dir
        self._done = False
        self._returned = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._done:
            if self._returned > self._check:
                raise Exception
            raise StopIteration
        
        retval = self._current
        if self._stop == retval:
            self._done = True
            return retval
        
        self._current = self._going[0] + retval[0], self._going[1] + retval[1]
        self._returned = self._returned + 1
        return retval


if __name__ == "__main__":
    floor_map = {}
    with open("data.txt", "r") as f:
        for line in f:
            points = line_re.match(line)
            x1, y1, x2, y2 = points.group(1), points.group(2), points.group(3), points.group(4)
            if not (x1 == x2 or y1 == y2):
                continue
            t = Thermal(int(x1), int(y1), int(x2), int(y2))
            for coord in t:
                count = floor_map.get(coord)
                if count is None:
                    floor_map[coord] = 1
                else:
                    floor_map[coord] = count + 1

    sum = 0
    for coord, count in floor_map.items():
        if count > 1:
            sum = sum + 1
    print(sum)

