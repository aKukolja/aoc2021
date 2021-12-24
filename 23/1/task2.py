from collections import defaultdict
from typing import NamedTuple
from math import inf
import heapq


"""
Layout

H  H     H     H     H     H   H
0  1  2  3  4  5  6  7  8  9  10
     11    13    15    17
     12    14    16    18

"""

SHRIMP_ROOMS = {
    'A': [11, 12],
    'B': [13, 14],
    'C': [15, 16],
    'D': [17, 18]
}
SHRIMP_COST = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000
}
HALLWAY = {0, 1, 3, 5, 7, 9, 10}
NEIGHBOURS = {
    0:  {1},
    1:  {0, 2},
    2:  {1, 3, 11},
    3:  {2, 4},
    4:  {3, 5, 13},
    5:  {4, 6},
    6:  {5, 7, 15},
    7:  {6, 8},
    8:  {7, 9, 17},
    9:  {8, 10},
    10: {9},
    11: {2, 12},
    12: {11},
    13: {4, 14},
    14: {13},
    15: {6, 16},
    16: {15},
    17: {8, 18},
    18: {17},
}


class State(NamedTuple):

    cost: int
    world: tuple[str]

    def final(self) -> bool:
        solved = tuple(['.'] * 11 + ['A', 'A'] + ['B', 'B'] + ['C', 'C'] + ['D', 'D'])
        return solved == self.world


test = State(0, tuple(['.'] * 11 + ['B', 'A'] + ['C', 'D'] + ['B', 'C'] + ['D', 'A']))
data = State(0, tuple(['.'] * 11 + ['A', 'C'] + ['D', 'D'] + ['A', 'B'] + ['C', 'B']))
test2 = State(0, tuple(['.'] * 10 + ['B'] + ['.', 'A'] + ['C', 'D'] + ['B', 'C'] + ['D', 'A']))


def print_state(state: State):
    print("".join(state.world[:11]))
    for i in range(2):
        a = state.world[SHRIMP_ROOMS['A'][i]]
        b = state.world[SHRIMP_ROOMS['B'][i]]
        c = state.world[SHRIMP_ROOMS['C'][i]]
        d = state.world[SHRIMP_ROOMS['D'][i]]
        print("  {} {} {} {}".format(a, b, c, d))


def our_room_good(world: tuple[str], shrimp_pos: int) -> bool:
    shrimp_name = world[shrimp_pos]
    assert(shrimp_name in "ABCD")

    my_room = SHRIMP_ROOMS[shrimp_name]
    for i, ri in enumerate(my_room):
        if ri != shrimp_pos:
            continue
        below_us = my_room[i+1:]
        m = (map(lambda si: world[si] == shrimp_name, below_us))
        return all(m)
    # shrimp not in room
    return False


def our_room_position(world: tuple[str], shrimp_pos: int) -> int | None:
    shrimp_name = world[shrimp_pos]
    assert(shrimp_name in "ABCD")
    room_indices = SHRIMP_ROOMS[shrimp_name]
    room = world[room_indices[0]: room_indices[-1] + 1]
    split_at = None
    for i, space in enumerate(room):
        if space != '.':
            split_at = i
            break
    if split_at is None:
        # all spaces empty
        return room_indices[-1]
    empty, full = room_indices[:split_at], room_indices[split_at:]
    if len(empty) == 0:
        # all spaces taken
        return None
    if all(map(lambda ri: world[ri] == shrimp_name, full)):
        # all shrimps in room are our guys, return bottom empty space
        return empty[-1]
    return None


def replace(world: tuple[str], shrimp_pos: int, destination: int) -> tuple[str]:
    assert(world[destination] == '.')
    assert(world[shrimp_pos] in "ABCD")
    workable = list(world)
    workable[destination] = workable[shrimp_pos]
    workable[shrimp_pos] = '.'
    return tuple(workable)


def _dfs(world: tuple[str], current: int, target: int, visited: set) -> int | None:
    if current == target:
        return 0
    if current in visited:
        return None
    visited.add(current)
    for neighbour in NEIGHBOURS[current]:
        if world[neighbour] != '.':
            continue
        distance = _dfs(world, neighbour, target, visited)
        if distance is not None:
            return 1 + distance
    return None


def dfs(world: tuple[str], start: int, end: int) -> int | None:
    return _dfs(world, start, end, set())


def legal_states(state: State):
    for shrimp_pos, shrimp in enumerate(state.world):
        if shrimp == '.':
            # shrimp is not shrimp
            continue
        # shrimp is in fact a shrimp

        # if shrimp is in his room and all others are, do not move
        if our_room_good(state.world, shrimp_pos):
            continue

        if shrimp_pos not in HALLWAY:
            for hall_pos in HALLWAY:
                if state.world[hall_pos] == '.':
                    # this spot is free, move into it
                    distance = dfs(state.world, shrimp_pos, hall_pos)
                    if distance is None:
                        continue
                    new_cost = state.cost + SHRIMP_COST[shrimp] * distance
                    yield State(new_cost, replace(state.world, shrimp_pos, hall_pos))

        # this handles hall -> room and room -> room
        position = our_room_position(state.world, shrimp_pos)
        if position is not None:
            distance = dfs(state.world, shrimp_pos, position)
            # there is space for us in our room and there ar no other shrimps
            # can move out of the room to hallway
            if distance is not None:
                new_cost = state.cost + distance * SHRIMP_COST[shrimp]
                yield State(new_cost, replace(state.world, shrimp_pos, position))


def solve_dijkstra(start: State):
    """
    dist: dict[State, int] = defaultdict(lambda: inf)
    dist[start] = 0
    pq: list[State] = []
    heapq.heappush(pq, start)

    while pq:
        s = heapq.heappop(pq)
        if s.final():
            return s
        for v in legal_states(s):
            alt = v.cost
            if alt < dist[v]:
                dist[v] = alt
                heapq.heappush(pq, v)
    return None
    """
    costs = defaultdict(lambda: inf)
    costs[start] = 0
    pq: list[State] = []
    heapq.heappush(pq, start)

    while len(pq) > 0:
        state = heapq.heappop(pq)
        if state.final():
            return state
        if state.cost > costs[state]:
            continue
        for next_state in legal_states(state):
            if next_state.cost < costs[next_state]:
                costs[next_state] = next_state.cost
                heapq.heappush(pq, next_state)
    return None


"""
print_state(test2)
print(our_room_good(test2.world, 12))
"""

if __name__ == "__main__":
    print(solve_dijkstra(data))
