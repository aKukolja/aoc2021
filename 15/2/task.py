import math
from collections import defaultdict
from collections import PriorityQueue as q


class Maze:

    def __init__(self):
        self._maze = []
        self._width = None
        self._height = 0
        self._kernel = [(-1, 0), (+1, 0), (0, -1), (0, +1)]
        self._factor = 1
        self._original_height = 0
        self._original_width = None

    def expand(self, n):
        self._factor = n
        self._width *= n
        self._height *= n
        self._end = self._height - 1, self._width - 1

    def _get_cost(self, neighbour):
        row, column = neighbour
        row_in_maze, row_factor = row % self._original_height, int(row / self._original_height)
        col_in_maze, col_factor = column % self._original_height, int(column / self._original_height)
        base_cost = self._maze[row_in_maze][col_in_maze]
        bumped_cost = base_cost + row_factor + col_factor
        overflow = bumped_cost % 9
        if overflow != 0:
            return overflow
        return bumped_cost
    
    def _bounds(self, coord):
        row, column = coord
        if row < 0  or row >= self._height:
            return False
        if column < 0 or column >= self._width:
            return False
        return True

    def add_nodes(self, weights):
        if self._width is None:
            self._width = len(weights)
            self._original_width = self._width
        if self._width != len(weights):
            raise Exception()

        self._maze.append(list(map(int, weights)))
        self._height += 1
        self._original_height = self._height
        self._start = 0, 0
        self._end = self._height - 1, self._width - 1

    def _check_neighbours(self, node, visited, distance_to, visit_candidates):
        all_checked = True
        row, column = node
        neighbours = filter(self._bounds, ((row + x, column + y) for x, y in self._kernel))
        for neighbour in neighbours:
            if neighbour in visited:
                continue
            all_checked = False
            n_row, n_col = neighbour
            cost = self._get_cost(neighbour)
            " this is reachable in this case "
            distance = cost + distance_to[node]
            if distance < distance_to[neighbour]:
                distance_to[neighbour] = distance
            assert(distance_to[neighbour] != math.inf)
            visit_candidates.add(neighbour)
        return all_checked

    def dijsktra(self):
        visited = { self._start }
        in_consideration = { self._start }
        distance_to = defaultdict(lambda: math.inf)
        distance_to[self._start] = 0
        while self._end not in visited:
            visit_candidates = set()
            check_no_longer = set()
            for node in in_consideration:
                " check available connection for each node in visited "
                if self._check_neighbours(node, visited, distance_to, visit_candidates):
                    check_no_longer.add(node)
            in_consideration = in_consideration.difference(check_no_longer)
            " pick out node to visit "
            # print(" ".join(map(str, visit_candidates)))
            decided = min(visit_candidates, key=lambda c: distance_to[c])
            visited.add(decided)
            in_consideration.add(decided)
        return distance_to[self._end]


if __name__ == "__main__":
    maze = Maze()
    with open("data.txt", "r") as f:
        for line in f:
            stripped = line.strip()
            maze.add_nodes(stripped)
    maze.expand(5)
    print(maze.dijsktra())

