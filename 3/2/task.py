
class Filter:

    def __init__(self):
        self._oxy = []
        self._co2 = []

    def add_line(self, line):
        self._oxy.append(line.strip())
        self._co2.append(line.strip())

    def _iterate_oxy(self, column):
        keep_oxy = []
        s = Summator(column)
        for number in self._oxy:
            s.add_line(number)
        common = s.most_common()
        for number in self._oxy:
            if number[column] == common:
                keep_oxy.append(number)
        self._oxy = keep_oxy
        if len(self._oxy) == 1:
            return True
        return False

    def _iterate_co2(self, column):
        keep_co2 = []
        s = Summator(column)
        for number in self._co2:
            s.add_line(number)
        common = s.least_common("0")
        for number in self._co2:
            if number[column] == common:
                keep_co2.append(number)
        self._co2 = keep_co2
        if len(self._co2) == 1:
            return True
        return False

    def solution(self):
        for i in range(len(self._oxy[0])):
            if self._iterate_oxy(i):
                break
        for i in range(len(self._co2[0])):
            if self._iterate_co2(i):
                break
        oxy = int(self._oxy[0], 2)
        co2 = int(self._co2[0], 2)
        print(oxy*co2)


class Summator:

    def __init__(self, column):
        self.array = None
        self.count = 0
        self.len = 0
        self._column = column

    def add_line(self, line):
        trimmed = line.strip()
        self.len = self.len + 1
        if line[self._column] == "1":
            self.count = self.count + 1

    def most_common(self, default="1"):
        if self.count == self.len/2:
            return default
        if self.count > self.len/2:
            return "1"
        return "0"

    def least_common(self, default="0"):
        if self.count == self.len/2:
            return default
        if self.count > self.len/2:
            return "0"
        return "1"


with open("data.txt", "r") as f:
    s = Filter()
    for line in f:
        s.add_line(line)
    s.solution()
