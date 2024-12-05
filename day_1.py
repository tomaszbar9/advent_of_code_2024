from download import data
from collections import Counter

d = data(1)
tps = []

for line in d.splitlines():
    i, j = line.split()
    tps.append((int(i), int(j)))

t1, t2 = zip(*tps)
tsort = zip(sorted(t1), sorted(t2))

result = 0
for v1, v2 in tsort:
    result += abs(v1 - v2)
print(result)

right_dict = Counter(t2)

result = 0
for n in t1:
    result += n * right_dict[n]
print(result)
