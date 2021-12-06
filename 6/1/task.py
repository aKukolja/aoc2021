class Fish:

    def __init__(self, number):
        self._number = number

    def multiply(self):
        self._number = self._number - 1
        if self._number == -1:
            self._number = 6
            return Fish(8)
        return None


with open("data.txt", "r") as f:
    school = []
    for line in f:
        for fish in line.split(","):
            school.append(Fish(int(fish)))
    for _ in range(80):
        newborn = []
        for fish in school:
            child = fish.multiply()
            if child is not None:
                newborn.append(child)
        school = school + newborn

    print(len(school))
