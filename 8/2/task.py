


digit_to_segments = {
    0: {c for c in "abcefg"},
    1: {c for c in "cf"},
    2: {c for c in "acdeg"},
    3: {c for c in "acdfg"},
    4: {c for c in "bcdf"},
    5: {c for c in "abdfg"},
    6: {c for c in "abdefg"},
    7: {c for c in "acf"},
    8: {c for c in "abcdefg"},
    9: {c for c in "abcdfg"},
}


len_to_digit = {
    2: {1},
    3: {7},
    4: {4},
    5: {2, 3, 5},
    6: {0, 6, 9},
    7: {8},
}


class Case:

    def _add_by_len(self, llen, sset):
        has = self._by_len.get(llen)
        if has is None:
            self._by_len[llen] = [sset]
        else:
            self._by_len[llen].append(sset)

    def __init__(self, uniques, display):
        self._solution = [None] * 10
        self._by_len = dict()
        for unique in uniques:
            if len(unique) == 2:
                self._solution[1] = unique
                continue
            if len(unique) == 3:
                self._solution[7] = unique
                continue
            if len(unique) == 4:
                self._solution[4] = unique
                continue
            if len(unique) == 7:
                self._solution[8] = unique
                continue
            self._add_by_len(len(unique), unique)
        assert(self._solution[1] is not None)
        assert(self._solution[7] is not None)
        assert(self._solution[8] is not None)
        assert(self._solution[4] is not None)
        assert(len(self._by_len[6]) == 3)
        assert(len(self._by_len[5]) == 3)
        self._display = display

    @staticmethod
    def _get_single(sset):
        if len(sset) != 1:
            print(sset)
            raise Exception
        for i in sset:
            return i

    def solve(self):
        remap = {k: None for k in "abcdefg"}
        remap['a'] = Case._get_single(self._solution[7] - self._solution[1])

        # find combination for 6 by subtracting 7
        for sset in self._by_len[6]:
            diff = sset - self._solution[7]
            if len(diff) == 4:
                assert(self._solution[6] is None)
                self._solution[6] = sset
                break
        assert(self._solution[6] is not None)
        self._by_len[6].remove(self._solution[6])

        # find combination for 0 & 9 by subracting 4
        for sset in self._by_len[6]:
            diff = sset - self._solution[4]
            if len(diff) == 3:
                assert(self._solution[0] is None)
                self._solution[0] = sset
            if len(diff) == 2:
                assert(self._solution[9] is None)
                self._solution[9] = sset
        assert(self._solution[9] is not None)
        assert(self._solution[0] is not None)

        # find combination of 3 by subtracting 7
        for sset in self._by_len[5]:
            diff = sset - self._solution[7]
            if len(diff) == 2:
                assert(self._solution[3] is None)
                self._solution[3] = sset
                break
        assert(self._solution[3] is not None)
        self._by_len[5].remove(self._solution[3])

        # find combination of 2 & 5 by subtracting 4
        for sset in self._by_len[5]:
            diff = sset - self._solution[4]
            if len(diff) == 3:
                assert(self._solution[2] is None)
                self._solution[2] = sset
            if len(diff) == 2:
                assert(self._solution[5] is None)
                self._solution[5] = sset
        assert(self._solution[5] is not None)
        assert(self._solution[2] is not None)
        

    def number(self):
        comb_to_num = {sset: i for i, sset in enumerate(self._solution)}
        retval = 0
        for comb in self._display:
            retval = retval * 10 + comb_to_num[comb]
        return retval


if __name__ == "__main__":
    collection = []
    with open("data.txt", "r") as f:
        for line in f:
            left, right = line.strip().split("|")
            left = left.strip()
            right = right.strip()
            uniques = {frozenset(x.strip()) for x in left.split()}
            displayed = [frozenset(x.strip()) for x in right.split()]
            collection.append(Case(uniques, displayed))
    sum = 0
    for case in collection:
        case.solve()
        sum = sum + case.number()
    print(sum)

