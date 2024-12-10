from download import data
from functools import lru_cache

d = data(10)
d = [[int(char) for char in line] for line in d.splitlines()]
size = len(d)
assert size == len(d[0])

def get_available_steps(position):
    directions = (-1, 0), (0, 1), (1, 0), (0, -1)
    steps = []
    valid_range = range(0, size)
    for di in directions:
        x0, x1 = di[0] + position[0], di[1] + position[1]
        if x0 in valid_range and x1 in valid_range:
            steps.append((x0, x1))
    return steps

def get_value(position):
    return d[position[0]][position[1]]

def find_nines(position):
    v = get_value(position)
    if v == 9:
        return {position}
    trails = set()
    for step in get_available_steps(position):
        if get_value(step) == v + 1:
            trails |= find_nines(step)
    return trails

result = 0
for i, line in enumerate(d):
    for j, val in enumerate(line):
        if val == 0:
            result += len(find_nines((i, j)))
print(result)

@lru_cache
def find_distinct_trails(position):
    v = get_value(position)
    if v == 9:
        return 1
    trails = 0
    for step in get_available_steps(position):
        if get_value(step) == v + 1:
            trails += find_distinct_trails(step)
    return trails

result = 0
for i, line in enumerate(d):
    for j, val in enumerate(line):
        if val == 0:
            result += find_distinct_trails((i, j))
print(result)
