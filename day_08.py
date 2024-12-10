from collections import defaultdict
from itertools import permutations
import numpy as np
from download import data

d = data(8)
d = d.splitlines()
antennas = defaultdict(list)
size = len(d)
assert size == len(d[0])

for i, l in enumerate(d):
    for j, c in enumerate(l):
        if c != ".":
            antennas[c].append(np.array([i, j]))

antinodes = set()
for values in antennas.values():
    pairs = permutations(values, 2)
    for i, j in pairs:
        antinode = i + (i - j)
        if np.isin(antinode, range(size)).all():
            antinodes.add(tuple(antinode))
print(len(antinodes))

for values in antennas.values():
    pairs = permutations(values, 2)
    for i, j in pairs:
        diff = i - j
        antinode = i.copy()
        while np.isin(antinode, range(size)).all():
            antinodes.add(tuple(antinode))
            antinode += diff
print(len(antinodes))
