
class Node:

    def __init__(self, name):
        self.name = name
        # if name == "start" or name == "end":
        #     self.is_small = False
        # else:
        self.is_small = all(map(lambda c: c.islower(), self.name))
        self.connections = set()

    def __str__(self):
        retval = self.name + " -> "
        for c in self.connections:
            retval = retval + c.name + ", "
        return retval

    def connect(self, node):
        self.connections.add(node)


class Caves:

    def __init__(self):
        self._start = None
        self._end = None
        self._nodes = dict()
        self._solutions = 0

    def add(self, line):
        left, right = line.split("-")

        left_node = self._nodes.get(left)
        if left_node is None:
            left_node = Node(left)
            self._nodes[left] = left_node
        if left == "start":
            self._start = left_node
        if left == "end":
            self._end = left_node

        right_node = self._nodes.get(right)
        if right_node is None:
            right_node = Node(right)
            self._nodes[right] = right_node
        if right == "start":
            self._start = right_node
        if right == "end":
            self._end = right_node

        right_node.connect(left_node)
        left_node.connect(right_node)

    def __str__(self):
        retval = str(self._solutions) + "\n"
        for name, node in self._nodes.items():
            retval = retval + str(node) + "\n"
        return retval

    def _for_node(self, node, path_ordered, smol_visited):
        path_ordered.append(node)
        if node.is_small:
            smol_visited.add(node)
        
        if node.name == "end":
            self._solutions = self._solutions + 1
            # print(",".join(map(lambda x: str(x.name), path_ordered)))
        else:
            for c in node.connections:
                " smol "
                if c in smol_visited:
                    continue
                self._for_node(c, path_ordered, smol_visited)

        if node.is_small:
            smol_visited.remove(node)
        path_ordered.pop()

    def solve(self):
        self._solutions = 0
        path_ordered = []
        smol_visited = set()
        self._for_node(self._start, path_ordered, smol_visited)


if __name__ == "__main__":
    caves = Caves()
    with open("data.txt", "r") as f:
        for line in f:
            caves.add(line.strip())
    caves.solve()
    print()
    print(caves)

