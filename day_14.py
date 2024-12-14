import re
from collections import Counter
import numpy as np
from download import data

d = data(14).splitlines()
WIDTH, HEIGHT = 101, 103

robots = []
pattern = re.compile(r"(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")
for line in d:
    p0, p1, v0, v1 = [int(x) if not x.startswith("-") else int(x[1:]) * -1 
               for x in pattern.findall(line)[0]]
    robots.append([[p0, p1], (v0, v1)])

for _ in range(100):
    for pos, vel in robots:
        pos[0] = (pos[0] + vel[0]) % WIDTH
        pos[1] = (pos[1] + vel[1]) % HEIGHT

vertical, horizontal = WIDTH // 2, HEIGHT // 2
quadrants = [[0, 0], [0, 0]]
for pos, _ in robots:
    if pos[0] == vertical or pos[1] == horizontal:
        continue
    i = pos[0] > vertical
    j = pos[1] > horizontal
    quadrants[j][i] += 1

total = 1
for x in sum(quadrants, []):
    total *= x
print(total)

r, v = [], []
for i, (rob, vel) in enumerate(robots):
    r.append(rob)
    v.append(vel)
r = np.array(r)
v = np.array(v)

def print_robots(r):
    positions = [tuple(x) for x in r]
    c = Counter(positions)
    for i in range(HEIGHT):
        row = []
        for j in range(WIDTH):
            if (j, i) in c:
                row.append(str(c[(j, i)]))
            else:
                row.append(".")
        print("".join(row))

def get_std(array):
    col_count = np.unique_counts(array[:, 0]).counts
    row_count = np.unique_counts(array[:, 1]).counts
    return np.std(np.hstack([col_count, row_count]))

# Get standard deviation of 10 000 consecutive arrays
std = []
rcopy = r.copy()
for _ in range(10_000):
    std.append(get_std(rcopy))
    rcopy = rcopy + v
    rcopy[:, 0] = rcopy[:, 0] % WIDTH
    rcopy[:, 1] = rcopy[:, 1] % HEIGHT
mean_std = np.mean(std)

for i in range(20_000):
    cur_std = get_std(r)
    if cur_std > 3 * mean_std:
        print(i)
        print_robots(r)
    r = r + v
    r[:, 0] = r[:, 0] % WIDTH
    r[:, 1] = r[:, 1] % HEIGHT
