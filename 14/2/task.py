from collections import defaultdict
import re


class Polymer:

    def __init__(self, sequence):
        self._pairs = defaultdict(lambda: 0)
        for pair in zip(sequence, sequence[1:]):
            self._pairs[pair] += 1
        self._rules = dict()
        self._regex = re.compile("^([A-Z])([A-Z]) -> ([A-Z])$")
        self._counter = defaultdict(lambda: 0)
        #print(sequence)
        for s in sequence:
            self._counter[s] += 1

    def add_rule(self, rule):
        match = self._regex.match(rule)
        assert(match is not None)
        self._rules[(match.group(1), match.group(2))] = match.group(3)

    def solve(self, steps):
        for _ in range(steps):
            new_pairs = defaultdict(lambda: 0)
            for pair, occurances in self._pairs.items():
                new_s = self._rules[pair]
                left_pair, right_pair = (pair[0], new_s), (new_s, pair[1])
                self._counter[new_s] += occurances
                new_pairs[left_pair] += occurances
                new_pairs[right_pair] += occurances
            self._pairs = new_pairs
        biggest = max(self._counter.values())
        smallest = min(self._counter.values())
        return biggest - smallest


if __name__ == "__main__":
    with open("data.txt", "r") as f:
        polymer = None
        for line in f:
            stripped = line.strip()
            polymer = Polymer(stripped)
            break
        for line in f:
            break
        for line in f:
            stripped = line.strip()
            polymer.add_rule(stripped)

        print(polymer.solve(40))


