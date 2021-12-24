from math import inf
from collections import defaultdict

rooms = {
    (2, 3): 'A', (3, 3): 'A',
    (2, 5): 'B', (3, 5): 'B',
    (2, 7): 'C', (3, 7): 'C',
    (2, 9): 'D', (3, 9): 'D'
}


costs = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000
}


class Shrimp:

    def __init__(self, name):
        self._name = name
        self._moved = 0
        self._cost = costs[name]

    def move(self):
        self._moved += 1

    def unmove(self):
        self._moved -= 1

    def moved(self):
        return self._moved

    def cost(self):
        return self._cost

    def name(self):
        return self._name

    def __str__(self):
        return self._name


class Room:

    def __init__(self, name, size, top_to_bottom):
        self._name = name
        self._size = size
        self._stack = list(reversed(top_to_bottom))

    def state(self):
        if len(self._stack) == 2:
            return tuple(self._stack)
        if len(self._stack) == 1:
            return None, self._stack[0]
        return None, None

    def free(self):
        return all(map(lambda o: o == self._name, self._stack))

    def done(self):
        return len(self._stack) == 2 and all(map(lambda o: o == self._name, self._stack))

    def shrimps(self):
        return [s for s in self._stack]

    def can_stay(self, shrimp):
        if shrimp.name() != self._name:
            return False
        if len(self._stack) == 2 and shrimp == self._stack[1]:
            if self._stack[0].name() == self._name:
                return True
            else:
                return False
        if len(self._stack) == 1 and shrimp == self._stack[0]:
            return True
        return False

    def __str__(self):
        return "".join(map(str, reversed(self._stack)))


class Hall:

    def __init__(self, a: Room, b: Room, c: Room, d: Room):
        self._state = [None] * 11
        self._a = a
        self._b = b
        self._c = c
        self._d = d
        self._shrimps = self._a.shrimps() + self._b.shrimps() + self._c.shrimps() + self._c.shrimps()
        self._go_low = {
            2: self._a, 4: self._b, 6: self._c, 8: self._d
        }

    def _state(self):
        return tuple(self._state), self._a.state(), self._b.state(), self._c.state(), self._d.state()

    def _can_stay(self, shrimp):
        room = {
            'A': self._a,
            'B': self._b,
            'C': self._c,
            'D': self._d,
        }[shrimp.name()]
        return room.can_stay(shrimp)

    def _solve(self):
        # if all shrimps are in place complete
        if self._a.done() and self._b.done() and self._c.done() and self._d.done():
            return 0
        for shrimp in self._shrimps:
            # if the shrimp can stay do not move it
            if self._can_stay(shrimp):
                continue
            if shrimp.moved() == 1:
                # shrimp was moved already
                pass
            else:
                # shrimp was not moved
                options = self._options(shrimp)
                pass

    def solve(self):
        # Depth First Search
        for shrimp in self._shrimps:
            # if room is free, move shrimp to room
            # if the shrimp moved skip it
            # if the shrimp has not moved, move it
            pass


        return 0

    def __str__(self):
        retval = "".join(map(lambda x: "." if x is None else x.name(), self._state))
        retval += "\n"
        a = str(self._a)
        b = str(self._b)
        c = str(self._c)
        d = str(self._d)
        retval += "  " + a[0] + " " + b[0] + " " + c[0] + " " + d[0] + "\n"
        retval += "  " + a[1] + " " + b[1] + " " + c[1] + " " + d[1] + "\n"
        return retval


test = Hall(
    Room('A', 2, [Shrimp('B'), Shrimp('A')]),
    Room('B', 2, [Shrimp('C'), Shrimp('D')]),
    Room('C', 2, [Shrimp('B'), Shrimp('C')]),
    Room('D', 2, [Shrimp('D'), Shrimp('A')]),
)

print(test)


animal_rooms = {
    'A': [(2, 3), (3, 3)],
    'B': [(2, 5), (3, 5)],
    'C': [(2, 7), (3, 7)],
    'D': [(2, 9), (3, 9)],
}


def can_move(world, animal_name):
    all(map(lambda c: world[c] == '.' or world[c] == animal_name, animal_rooms[animal_name]))


forbidden = {(1, 3), (1, 5), (1, 7), (1, 9)}

data = [
    "#############",
    "#...........#",
    "###A#D#A#C###",
    "###C#D#B#B###",
    "#############"
]

test = [
    "#############",
    "#...........#",
    "###B#C#B#D###",
    "###A#D#C#A###",
    "#############"
]


def no_collision(world, animal: tuple):
    # left, right, up, down
    row, col = animal
    kernel = [(0, -1), (0, +1), (-1, 0), (1, 0)]

    def f(c):
        return world[c] == '.'

    candidates = [(row + y, col + x) for y, x in kernel]
    return filter(f, candidates)


def can_room(animal_name, option):
    assert(animal_name in "ABCD")
    if option not in rooms.keys():
        return True
    if option in animal_rooms[animal_name]:
        print("True")
        return True
    return False


def possible_stops(world: dict, animal_name, cost: int, position: tuple, entered: dict, checked: set):
    if position in checked:
        return
    checked.add(position)
    candidates = filter(lambda c: c not in checked, no_collision(world, position))
    for candidate in candidates:
        if candidate not in forbidden and can_room(animal_name, candidate):
            entered[candidate] = cost + costs[animal_name]
        possible_stops(world, animal_name, cost + costs[animal_name], candidate, entered, checked)


def calc_cost(world, shrimps, moved: dict):
    test = True
    for room, target in rooms.items():
        assert(world[room] != '#')
        test = test and world[room] == target
    if test:
        return 0

    # if all(map(lambda shrimp: world[shrimp] == rooms.get(shrimp), shrimps)):
    #     return 0
    if shrimps == moved:
        # all shrimps moved and we are not finished
        return inf
    # move each shrimp that wasn't moved

    best_cost = inf
    for s in shrimps.difference(moved):
        shrimp_name = world[s]
        positions = dict()
        possible_stops(world, shrimp_name, 0, s, positions, set())
        for new_position, move_cost in positions.items():
            # change world to reflect movement
            moved[new_position] = moved[s] + 1
            world[new_position] = shrimp_name
            world[s] = '.'
            shrimps.add(new_position)
            shrimps.remove(s)
            complete_cost = calc_cost(world, shrimps, moved) + move_cost
            best_cost = min(best_cost, complete_cost)
            # restore context
            shrimps.add(s)
            shrimps.remove(new_position)
            world[s] = shrimp_name
            world[new_position] = '.'
            moved.remove(new_position)
    return best_cost


def print_world(world, checked: dict):
    retval = ""
    for row, row_elements in enumerate(world):
        for col, element in enumerate(row_elements):
            coord = row, col
            if coord in checked.keys():
                retval += "|"
            else:
                retval += str(element)
        retval += "\n"
    print(retval)


if __name__ == "__main__":
    world_in = test
    m_world = defaultdict(lambda: '#')
    low_cost = inf
    m_shrimps = set()

    for m_row, row_val in enumerate(world_in):
        for m_col, val in enumerate(row_val):
            m_coord = m_row, m_col
            m_world[m_coord] = val
            if val in "ABCD":
                m_shrimps.add(m_coord)

    m_cost = calc_cost(m_world, m_shrimps, defaultdict(lambda: 0))
    print(m_cost)
    """
    possible = dict()
    possible_stops(m_world, 'B', 0, (2, 3), possible, set())
    print(possible)
    print_world(test, possible)
    """
