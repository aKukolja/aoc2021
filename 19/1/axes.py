from math import cos, sin, pi
import numpy as np
from itertools import product


def rotate_x(phi, v):
    rot = np.array([
        [int(cos(phi)), int(-sin(phi)), 0],
        [int(sin(phi)), int(cos(phi)), 0],
        [0, 0, 1]])
    return tuple(map(int, np.matmul(rot, np.array(v).T)))

def rotate_y(phi, v):
    rot = np.array([
        [int(cos(phi)), 0, int(sin(phi))],
        [0, 1, 0],
        [int(-sin(phi)), 0, int(cos(phi))]])
    return tuple(map(int, np.matmul(rot, np.array(v).T)))

def rotate_z(phi, v):
    rot = np.array([
        [1, 0, 0],
        [0, int(cos(phi)), int(-sin(phi))],
        [0, int(sin(phi)), int(cos(phi))]])
    return tuple(map(int, np.matmul(rot, np.array(v).T)))


solution = set()
original = (1, 2, 3)
angles = [0, pi/2, pi, -pi/2]
for xa, ya, za in product(angles, angles, angles):
    v = rotate_x(xa, original)
    v = rotate_y(ya, v)
    v = rotate_z(za, v)
    solution.add(v)

t = {1: "x", 2: "y", 3: "z"}
def tt(v):
    return ("" if v > 0 else "-") + t[abs(v)]
def ttt(xyz):
    x, y, z = xyz
    return "lambda: ( " + tt(x) + "," + tt(y) + "," + tt(z) + "),"

lol = map(lambda i: str(i[0]) + ": " + i[1], enumerate(map(ttt, solution)))
for oll in lol:
    print(oll)





