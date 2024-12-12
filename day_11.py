from collections import defaultdict
from download import data

d = data(11).split()

def transform(n):
    if n == "0":
        return "1",
    elif len(n) % 2 == 0:
        new_length = len(n) // 2
        left, right = n[:new_length], n[new_length:]
        right = right.lstrip("0")
        if not right:
            right = "0"
        return left, right
    else:
        return str(2024 * int(n)),

def count_values(counter:dict):
    result = 0
    for v in counter.values():
        result += v
    return result

# Initiate counter
counter = defaultdict(int)
for item in d:
    counter[item] += 1

for i in range(75):
    temp = defaultdict(int)
    for item, factor in counter.items():
        transformed = transform(item)
        for t in transformed:
            temp[t] += factor
    counter = temp
    if i == 24:
        print(count_values(counter))

print(count_values(counter))
