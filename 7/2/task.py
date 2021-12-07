
def trianglo(start, end):
    retval = start - end
    retval = retval * retval + abs(retval)
    retval = retval / 2
    return retval


class CrabArray:

    def __init__(self):
        self._crabs = {}
        self._start = None
        self._stop = None

    def add_crab(self, distance):
        crab_count = self._crabs.get(distance)
        if crab_count is None:
            self._crabs[distance] = 1
        else:
            self._crabs[distance] = crab_count + 1
        if self._start is None:
            self._start = distance
        else:
            self._start = min(distance, self._start)
        if self._stop is None:
            self._stop = distance
        else:
            self._stop = max(distance, self._stop)

    @staticmethod
    def _find_rms(crabs, position):
        rms = 0
        for crab_position, crab_count in crabs.items():
            fuel_spent = trianglo(crab_position, position) * crab_count
            rms = rms + fuel_spent
        return rms

    @staticmethod
    def _crab_mean(crabs):
        sum = 0
        total_crabs = 0
        for distance, count in crabs.items():
            sum = sum + distance * count
            total_crabs = total_crabs + count
        return int(sum / total_crabs)

    def find_optimal_distance(self):
        mass = CrabArray._crab_mean(self._crabs)
        possible = {mass - 1, mass, mass + 1}
        all_solutions = {}
        for position in possible:
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
