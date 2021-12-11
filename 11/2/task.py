from itertools import product


class Cave:

    def __init__(self):
        self._octi = []
        self._height = 0
        self._width = None
        self._all_coords = None
        self._kernel = {
            (-1, -1), (-1, 0), (-1, +1),
            (0, -1), (0, 1),
            (+1, -1), (+1, 0), (+1, +1),
        }

    def add_row(self, row):
        row_octi = [int(val) for val in row]
        width = len(row_octi)
        if self._width is None:
            self._width = width
        elif self._width != width:
            raise Exception
        self._octi.append(row_octi)
        self._height = self._height + 1
        self._all_coords = set(product(range(self._height), range(self._width)))

    def __str__(self):
        retval = ""
        for row in self._octi:
            for octo in row:
                retval = retval + str(octo)
            retval = retval + "\n"
        return retval

    def _bump(self, row, column):
        self._octi[row][column] = self._octi[row][column] + 1

    def _flash(self, row, column):
        val = self._octi[row][column]
        if val > 9:
            self._octi[row][column] = 0
            return True
        return False

    def _flash_check(self, to_check, flashed):
        for coord in to_check:
            if coord in flashed:
                continue
            row, column = coord
            if self._flash(row, column):
                flashed.add(coord)
                neighbours = [(row+c[0], column+c[1]) for c in self._kernel]
                neighbours = self._all_coords.intersection(neighbours)
                for n in neighbours:
                    if n in flashed:
                        continue
                    self._bump(n[0], n[1])
                self._flash_check(neighbours, flashed)

    def flash(self):
        for coord in self._all_coords:
            row, column = coord
            self._bump(row, column)
        flashed = set()
        self._flash_check(self._all_coords, flashed)
        return len(flashed)

    def count(self):
        return self._width * self._height


if __name__ == "__main__":
    cave = Cave()
    with open("data.txt", "r") as f:
        for line in f:
            cave.add_row(line.strip())
    sum = 0
    for i in range(10000):
        how_many = cave.flash()
        if how_many == cave.count():
            print(i+1)
            break
        sum = sum + how_many
    print(sum)
    print(cave)
