
class Map:

    def __init__(self):
        self._map = []
        self._kernel = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1),
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
            retvals.append(self._map[row][column])
        return retvals

    def find_lows(self):
        """
        return row, column, value, risk
        """
        lows = []
        for row_index, row in enumerate(self._map):
            for column_index, value in enumerate(row):
                kernel = [(row_index + x, column_index + y) for x, y in self._kernel]
                values = self._get_vals(kernel)
                if all(map(lambda x: value < x, values)):
                    lows.append((row_index, column_index, value, value + 1))

        return lows


if __name__ == "__main__":
    world = Map()
    with open("data.txt", "r") as f:
        for line in f:
            world.add_row(list(map(int, line.strip())))
    print(sum(map(lambda x: x[3], world.find_lows())))

