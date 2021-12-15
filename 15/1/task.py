import math
from collections import defaultdict


class Node:

    def __init__(self, coord, value):
        self.coord = coord
        self.weight = value
        self.connections = []

    def connect(self, node):
        connection = node.weight, node
        self.connections.append(connection)
        neighbour_connection = self.weight, self
        node.connections.append(neighbour_connection)
        assert(len(node.connections) <= 4)
        assert(len(self.connections) <= 4)


class Maze:

    def __init__(self):
        self._nodes = dict()
        self._width = None
        self._height = 0
        self._kernel = [(-1, 0), (+1, 0), (0, -1), (0, +1)]

    def add_nodes(self, weights):
        if self._width is None:
            self._width = len(weights)
        if self._width != len(weights):
            raise Exception()
        row = self._height
        for column, val in enumerate(map(int, weights)):
            coord = row, column
            node = Node(coord, val)
            self._nodes[coord] = node
            " neighbours = [(row + x, column + y) for x, y in self._kernel] "
            for neighbour in [(row - 1, column), (row, column - 1)]:
                n_row, n_col = neighbour
                if n_row < 0:
                    continue
                if n_col < 0:
                    continue
                node.connect(self._nodes[neighbour])

        self._height += 1
        self._start = self._nodes[(0, 0)]
        self._end = self._nodes[(self._height - 1, self._width - 1)]

    def dijsktra(self):
        visited = { self._start }
        " distance_to = { node: 0 if node == self._start else math.inf for node in self._nodes.values() } "
        distance_to = defaultdict(lambda: math.inf)
        distance_to[self._start] = 0
        while self._end not in visited:
            visit_candidates = set()
            for node in visited:
                " check available connection for each node in visited "
                for cost, neighbour in node.connections:
                    if neighbour in visited:
                        continue
                    " this is reachable in this case "
                    distance = cost + distance_to[node]
                    if distance < distance_to[neighbour]:
                        distance_to[neighbour] = distance
                    assert(distance_to[neighbour] != math.inf)
                    visit_candidates.add(neighbour)
            " pick out node to visit "
            decided = min(visit_candidates, key=lambda c: distance_to[c])
            visited.add(decided)
        return distance_to[self._end]



if __name__ == "__main__":
    maze = Maze()
    with open("data.txt", "r") as f:
        for line in f:
            stripped = line.strip()
            maze.add_nodes(stripped)
    print(maze.dijsktra())

