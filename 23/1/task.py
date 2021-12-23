from math import inf
from collections import defaultdict

rooms = {
    (2, 3): 'A', (3, 3): 'A',
    (2, 5): 'B', (3, 5): 'B',
    (2, 7): 'C', (3, 7): 'C',
    (2, 9): 'D', (3, 9): 'D'
}

animal_rooms = {
    'A': [(2, 3), (3, 3)],
    'B': [(2, 5), (3, 5)],
    'C': [(2, 7), (3, 7)],
    'D': [(2, 9), (3, 9)],
}

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

costs = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000
}


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


def calc_cost(world, shrimps, moved: set):
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
            moved.add(new_position)
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

    m_cost = calc_cost(m_world, m_shrimps, set())
    print(m_cost)
    """
    possible = dict()
    possible_stops(m_world, 'B', 0, (2, 3), possible, set())
    print(possible)
    print_world(test, possible)
    """
