class World:

    def __init__(self):
        self._world = []
        self._width = 0
        self._height = 0

    def add_row(self, row: str) -> None:
        """
        vals = {
            ".": 0,
            ">": 1,
            "v": 2
        }
        converted = [vals[c] for c in row]
        """
        converted = [c for c in row]
        width = len(converted)
        if self._width == 0:
            self._width = width
        if width != self._width:
            raise Exception
        self._world.append(converted)
        self._height = len(self._world)

    def _next_location(self, current: tuple[int, int], direction: tuple[int, int]) -> tuple[int, int]:
        next_row = current[0] + direction[0]
        next_row = next_row % self._height
        next_col = current[1] + direction[1]
        next_col = next_col % self._width
        return next_row, next_col

    def _move_slugs(self, slug_type: str) -> int:
        direction = {
            '>': (0, 1),
            'v': (1, 0)
        }[slug_type]

        # find all movable slugs
        from_to = dict()
        for row_i, row in enumerate(self._world):
            for col_i, slug in enumerate(row):
                curr_loc = row_i, col_i
                next_loc = self._next_location(curr_loc, direction)
                if self._world[row_i][col_i] == slug_type and self._world[next_loc[0]][next_loc[1]] == '.':
                    assert(from_to.get(curr_loc) is None)
                    from_to[curr_loc] = next_loc

        # replace all found
        for origin, destination in from_to.items():
            o_row, o_col = origin
            d_row, d_col = destination
            self._world[o_row][o_col] = '.'
            self._world[d_row][d_col] = slug_type

        return len(from_to)

    def _move(self) -> int:
        slugs_moved = self._move_slugs('>')
        slugs_moved += self._move_slugs('v')
        return slugs_moved

    def solve(self) -> int:
        iterations = 1
        while self._move() != 0:
            iterations += 1
        return iterations

    def __str__(self):
        retval = ""
        for row_i in range(self._height):
            for col_i in range(self._width):
                retval += self._world[row_i][col_i]
            retval += "\n"
        return retval + "\n"


if __name__ == "__main__":
    world = World()
    with open("data.txt", "r") as f:
        for line in f:
            world.add_row(line.strip())
    print(world.solve())
