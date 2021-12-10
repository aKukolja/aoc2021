

class Pair:

    def __init__(self, opening):
        self._open = opening
        self._close = None
        self._pairs = {
            '<': '>',
            '(': ')',
            '[': ']',
            '{': '}',
            '-': '-'
        }
        self._score = 0

    def wants(self):
        return self._pairs[self._open]

    def close_it(self, closing):
        should_be = self._pairs[self._open]
        if not should_be == closing:
            return False
        self._close = closing
        return True


class Machine:

    def __init__(self, line):
        self._line = line.strip()
        self._symbols = [s for s in self._line]
        self._stack = []
        " push sentinel on stack "
        self._stack.append(Pair('-'))
        self._opening = {s for s in "(<[{"}

    def complete(self):
        score_table = {
            ')': 1,
            ']': 2,
            '}': 3,
            '>': 4,
        }
        for s in self._symbols:
            if s in self._opening:
                self._stack.append(Pair(s))
            else:
                latest = self._stack[-1]
                if not latest.close_it(s):
                    return None
                else:
                    self._stack.pop()

        closers = []
        while len(self._stack) > 1:
            pair = self._stack.pop()
            chaser = pair.wants()
            closers.append(chaser)

        score = 0
        for closer in closers:
            score = score * 5 + score_table[closer]

        return score



if __name__ == "__main__":
    scores = []
    with open("data.txt", "r") as f:
        for line in f:
            machine = Machine(line)
            score = machine.complete()
            if score is not None:
                scores.append(machine.complete())
    print(sorted(scores)[len(scores)//2:][0])
