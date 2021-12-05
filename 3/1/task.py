class Summator:

    def __init__(self):
        self._array = None
        self._len = 0

    def add_line(self, line):
        trimmed = line.strip()
        if self._array is None:
            self._array = [ 0 ] * len(trimmed)
            self._len = 0
            print(trimmed, self._array, len(trimmed))
        self._len = self._len + 1
        for i, c in enumerate(trimmed):
            if c == "1":
                self._array[i] = self._array[i] + 1

    def solution(self):
        gamma_str = ""
        epsilon_str = ""
        if len(self._array) % 2 != 0:
            print(len(self._array))
        for count in self._array:
            if count > self._len/2:
                gamma_str = gamma_str + "1"
                epsilon_str = epsilon_str + "0"
            else:
                gamma_str = gamma_str + "0"
                epsilon_str = epsilon_str + "1"

        gamma = int(gamma_str, 2)
        epsilon = int(epsilon_str, 2)
        print(gamma_str, gamma)
        print(epsilon_str, epsilon)
        print("gama*epsilon =", gamma*epsilon)




with open("data.txt", "r") as f:
    s = Summator()
    for line in f:
        s.add_line(line)
    s.solution()
