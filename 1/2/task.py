from collections import deque


class Tuplet:

    def __init__(self, source, n, converter=None):
        self._converter = converter
        self._source = source
        self._array = deque()
        self._n = n
        for _ in range(self._n - 1):
            n = next(self._source)
            if n is None:
                break
            self._append(n)

    def _append(self, item):
        if self._converter is not None:
            item = self._converter(item)
        self._array.append(item)

    def __iter__(self):
        return self

    def __next__(self):
        n = next(self._source)
        if n is not None:
            self._append(n)
        retval = tuple(self._array)
        self._array.popleft()
        return retval


count = 0
with open("data.txt", "r") as f:
    t = Tuplet(f, 3, int)
    p = Tuplet(t, 2)

    for first, second in p:
        ff, ss = sum(first), sum(second)
        if ss > ff:
            count += 1

print(count)
