import re
from copy import deepcopy
from download import data
import numpy as np

d = data(13)
machines = d.split("\n\n")

ms = []
pattern = re.compile(r'X.(\d+), Y.(\d+)')
for machine in machines:
    ms.append([np.array([int(x) 
                         for x in pattern.findall(line)[0]]) 
               for line in machine.splitlines()])

count = 0
total = 0
ms1 = deepcopy(ms)
for a, b, p in ms1:
    count = 0
    while (p > 0).all():
        p -= a
        count += 3
        div, mod = divmod(p, b)
        if mod.any() == 0 and div[0] == div[1]:
            count += div
            total += count
            p -= div * b
            break
print(total[0])

a_lot = 10000000000000
for i, m in enumerate(ms):
    ms[i][2] = m[2][0] + a_lot, m[2][1] + a_lot

total = 0
for (ax, ay), (bx, by), (px, py) in ms:
    j = (ax * py - ay * px) / (ax * by - ay * bx)
    i = (px - bx * j) / ax
    if i - int(i) == 0 and j - int(j) == 0:
        i, j = int(i), int(j)
        total += 3 * i + j
print(total)
