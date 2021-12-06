class Fish:

    def __init__(self, number):
        self._number = number

    def multiply(self):
        self._number = self._number - 1
        if self._number == -1:
            self._number = 6
            return Fish(8)
        return None


class School:

    def __init__(self):
        self._school = {}

    def add_single(self, due_date):
        School._add_many(self._school, due_date, 1)

    @staticmethod
    def _add_many(school, due_date, fish_count):
        already_present = school.get(due_date)
        if already_present is None:
            school[due_date] = fish_count
        else:
            school[due_date] = already_present + fish_count

    def day_passes(self):
        new_school = {}
        for date_due in sorted(self._school.keys()):
            fish_due = self._school[date_due]
            new_due_date = date_due - 1
            if new_due_date == -1:
                School._add_many(new_school, 6, fish_due)
                # now add new fish
                School._add_many(new_school, 8, fish_due)
            else:
                School._add_many(new_school, new_due_date, fish_due)
        self._school = new_school

    def count(self):
        sum = 0
        for _, fish_count in self._school.items():
            sum = sum + fish_count
        return sum


with open("data.txt", "r") as f:
    school = School()
    for line in f:
        for fish in line.split(","):
            due_date = int(fish)
            school.add_single(due_date)
    for _ in range(256):
        school.day_passes()

    print(school.count())
