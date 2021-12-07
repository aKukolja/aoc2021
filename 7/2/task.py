
def trianglo(start, end):
    retval = start - end
    retval = retval * retval + abs(retval)
    retval = retval / 2
    return retval


class CrabArray:

    def __init__(self):
        self._crabs = {}

    def add_crab(self, distance):
        crab_count = self._crabs.get(distance)
        if crab_count is None:
            self._crabs[distance] = 1
        else:
            self._crabs[distance] = crab_count + 1

    @staticmethod
    def _find_rms(crabs, position):
        rms = 0
        for crab_position, crab_count in crabs.items():
            fuel_spent = trianglo(crab_position, position) * crab_count
            rms = rms + fuel_spent
        return rms

    def find_optimal_distance(self):
        starting_distances = self._crabs.keys()
        start = min(starting_distances)
        stop = max(starting_distances)
        all_solutions = {}

        for position in range(start, stop + 1):
            all_solutions[position] = CrabArray._find_rms(self._crabs, position)

        solution = min(all_solutions.items(), key=lambda x: x[1])

        return solution


if __name__ == "__main__":
    crabs = CrabArray()
    with open("data.txt", "r") as f:
        for line in f:
            for position in line.strip().split(","):
                crabs.add_crab(int(position))

    print(crabs.find_optimal_distance())
