from collections import defaultdict
from itertools import combinations
import numpy as np
from download import data

d = data(12)

def count_corners(current, neighbours, plants):
    neighbours = [np.array(n) for n in neighbours]
    c = np.array(current)
    match len(neighbours):
        case 0:
            return 4
        case 1:
            return 2
        case 2:
            p0, p1 = neighbours
            if ((p0 + p1) == c * 2).all():
                return 0
            if tuple(p0 + p1 - c) in plants:
                return 1
            return 2
        case _:
            pairs = combinations(neighbours, 2)
            corners = 0
            for p0, p1 in pairs:
                between = p0 + p1 - c
                if tuple(between) not in plants:
                    corners += 1
            return corners
plants = defaultdict(set)

for i, line in enumerate(d.splitlines()):
    for j, char in enumerate(line):
        plants[char].add((i, j))

directions = (-1, 0), (0, 1), (1, 0), (0, -1)
perimeters, areas, corners = [], [], []
for plant in plants.values():
    current_plant = plant.copy()
    while plant:
        deck = [plant.pop()]
        perimeters.append(0)
        areas.append(1)
        corners.append(0)
        idx = len(perimeters) - 1
        while deck:
            field = deck.pop()
            neighbours = []
            addresses = set((field[0] + d[0], field[1] + d[1]) for d in directions)
            all_neighbours = addresses & current_plant
            for address in addresses:
                if address in plant:
                    deck.append(address)
                    areas[idx] += 1
                    plant.remove(address)
            perimeters[idx] += (4 - len(all_neighbours))
            corners[idx] += count_corners(field, 
                                          all_neighbours, 
                                          current_plant)

print(sum([i * j for i, j in zip(perimeters, areas)]))
print(sum([i * j for i, j in zip(corners, areas)]))
