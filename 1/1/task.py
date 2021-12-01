class Pairs:

    def __init__(self, file):
        self._file = file
        self._first = next(file)

    def __iter__(self):
        return self

    def __next__(self):
        second = next(self._file)
        if self._first is None or second is None:
            return None
        pair = self._first, second
        self._first = second
        return pair


count = 0
with open("data.txt", "r") as f:
    p = Pairs(f)
    for first, second in p:
        ff, ss = int(first), int(second)
        if ss > ff:
            count += 1

print(count)
