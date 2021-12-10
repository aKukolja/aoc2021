

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

    def check(self):
        score_table = {
            ')': 3,
            ']': 57,
            '}': 1197,
            '>': 25137,
        }
        for s in self._symbols:
            if s in self._opening:
                self._stack.append(Pair(s))
            else:
                latest = self._stack[-1]
                if not latest.close_it(s):
                    return score_table[s]
                else:
                    self._stack.pop()
        return 0



if __name__ == "__main__":
    sum = 0
    with open("data.txt", "r") as f:
        for line in f:
            machine = Machine(line)
            sum = sum + machine.check()
    print(sum)
