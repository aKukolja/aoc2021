from itertools import product
from functools import reduce

class Map:

    def __init__(self):
        self._map = []
        self._kernel = [
            (-1, 0),
            (0, -1), (0, 1),
            (1, 0),
        ]
        self._height = 0
        self._width = None


    def add_row(self, fields):
        row_width = len(fields)
        if self._width is None:
            self._width = row_width
        elif row_width != self._width:
            raise Exception
        self._map.append(fields)
        self._height = self._height + 1

    def __str__(self):
        retval = ""
        for row in self._map:
            retval = retval + str(row) + "\n"
        return retval

    def _get_vals(self, kernel):
        retvals = []
        for row, column in kernel:
            if row < 0 or row >= self._height:
                continue
            if column < 0 or column >= self._width:
                continue
            retvals.append(((row, column), self._map[row][column]))
        return retvals

    def _inspect_basin(self, this_coord, basin):
        " alway called on a part of basin  "
        "add yourself to checked  "
        row_index, column_index = this_coord
        basin.add(this_coord)

        " find neighbouring cells "
        neighbours = [(row_index + x, column_index + y) for x, y in self._kernel]
        " exclude those who were already checked "
        neighbours = filter(lambda x: x not in basin, neighbours)
        " get their values "
        n_values = self._get_vals(neighbours)

        for coord, value in n_values:
            if value > self._map[row_index][column_index] and value < 9:
                self._inspect_basin(coord, basin)
            
        return basin

    def find_basins(self):
        """
        return row, column, value, risk
        """
        all_coords = product(range(self._height), range(self._width))
        basins = []
        confirmed = set()
        for row_index, column_index in all_coords:
            if (row_index, column_index) in confirmed:
                continue
            value = self._map[row_index][column_index]
            kernel = [(row_index + x, column_index + y) for x, y in self._kernel]
            values = self._get_vals(kernel)
            if all(map(lambda x: value < x[1], values)):
                basin = set()
                self._inspect_basin((row_index, column_index), basin)
                basins.append(basin)
                confirmed = confirmed.union(basin)
        return basins


if __name__ == "__main__":
    world = Map()
    with open("data.txt", "r") as f:
        for line in f:
            world.add_row(list(map(int, line.strip())))
    print(reduce(lambda x, y: x*y, sorted(map(lambda x: len(x), world.find_basins()), reverse=True)[:3]))
    "print(sum(map(lambda x: x[3], world.find_basin())))"

