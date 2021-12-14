import re


class Paper:

    def __init__(self):
        self._regex = re.compile("^fold along ([x|y])=(\\d+)$")
        self._paper = dict()
        self._height, self._width = 0, 0

    @staticmethod
    def _set_dot(paper, coord):
        paper[coord] = 1

    def add_dot(self, coord):
        x, y = coord
        " keep in mind taht coordingates start from 0, 0 "
        if x > self._width:
            self._width = x
        if y > self._height:
            self._height = y
        Paper._set_dot(self._paper, coord)

    def _vertical_seam(self, index):
        #print("vertical", index)
        next_paper = dict()
        for coord in self._paper:
            x, y = coord
            if x < index:
                new_coord = coord
            elif x == index:
                continue
            else:
                new_coord = 2 * index - x, y
            #print("moving", coord, "->", new_coord)
            Paper._set_dot(next_paper, new_coord)
        self._paper = next_paper
                

    def _horizontal_seam(self, index):
        #print("horizontal", index)
        next_paper = dict()
        for coord in self._paper:
            x, y = coord
            if y < index:
                new_coord = coord
            elif y == index:
                continue
            else:
                new_coord = x, 2 * index - y
            #print("moving", coord, "->", new_coord)
            Paper._set_dot(next_paper, new_coord)
        self._paper = next_paper

    def fold(self, command):
        match = self._regex.match(command)
        if match is None:
            raise Exception()
        action = {
            "y": self._horizontal_seam,
            "x": self._vertical_seam
        }[match.group(1)](int(match.group(2)))

    def count(self):
        return len(self._paper)


if __name__ == "__main__":
    paper = Paper()
    with open("data.txt", "r") as f:
        for line in f:
            stripped = line.strip()
            if stripped == "":
                break
            coord = tuple(map(int, stripped.split(",")))
            if len(coord) != 2:
                raise Exception()
            paper.add_dot(coord)
        for line in f:
            stripped = line.strip()
            paper.fold(stripped)
            print(paper.count())


