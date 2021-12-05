class Field:

    def __init__(self, name):
        self._set = False
        self._name = int(name)

    def name(self):
        return self._name

    def set(self):
        self._set = True

    def is_set(self):
        return self._set

    def __str__(self):
        return "<" + str(self._name) + ">"


class Board:

    def __str__(self):
        retval = ""
        for row in self._board:
            for field in row:
                retval = retval + "\t"
                if field.is_set():
                    retval = retval + str(field)
                else:
                    retval = retval + str(field.name())
            retval = retval + "\n"

        return retval

    def __init__(self, lines):
        if len(lines) != 5:
            raise Exception
        self._board = [
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None],
        ]
        for row, line in enumerate(lines):
            split = line.split()
            if len(split) != 5:
                raise Exception
            for column, number in enumerate(split):
                rrow = self._board[row]
                rrow[column] = Field(number)

    def check(self, number):
        for row, line in enumerate(self._board):
            for column, field in enumerate(line):
                if number == field.name():
                    field.set()
                    if self._check(row, column):
                        return row, column, number

    def score(self, call):
        sum = 0
        for row in self._board:
            for field in row:
                if not field.is_set():
                    sum = sum + field.name()
        print(self)
        print(sum, call)
        return sum * call

    def _check(self, row, column):
        if all(map(lambda x: x.is_set(), self._board[row])):
            return True
        if all(map(lambda x: x.is_set(), [f[column] for f in self._board])):
            return True


if __name__ == "__main__":
    sequence = []
    boards = []
    accumulator = []

    with open("data.txt", "r") as f:
        for i, line in enumerate(f):
            stripped = line.strip()
            if i == 0:
                sequence = map(int, line.split(","))
                continue
            if i == 1:
                continue
            if len(accumulator) == 5:
                boards.append(Board(accumulator))
                accumulator = []
            if len(stripped) == 0:
                continue
            else:
                accumulator.append(stripped)

    if len(accumulator) == 5:
            boards.append(Board(accumulator))

    def check_boards(boards, number):
        for board in boards:
            retval = board.check(number)
            if retval is not None:
                return board.score(number)
        return None


    for number in sequence:
        score = check_boards(boards, number)
        if score is not None:
            print(score)
            break

