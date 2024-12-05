import re
from download import data

d = data(3)

def get_numbers(s):
    pairs = re.findall(r'mul\((\d{1,3},\d{1,3})\)', s)
    numbers = []
    for pair in pairs:
        i, j = pair.split(",")
        numbers.append((int(i), int(j)))
    return numbers

result = sum([i * j for i, j in get_numbers(d)])
print(result)

pieces =  d.split("()")
on = True

result = 0
for piece in pieces:
    if on:
        pairs = re.findall(r'mul\((\d{1,3},\d{1,3})\)', piece)
        for pair in pairs:
            i, j = pair.split(",")
            result += int(i) * int(j)
    if piece.endswith("don't"):
        on = False
    if piece.endswith("do"):
        on = True
print(result)
