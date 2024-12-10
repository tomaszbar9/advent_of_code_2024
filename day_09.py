from download import data
from itertools import count

d = data(9)

def big_nums_gen(d):
    last_number = (len(d) - 1) // 2
    if len(d) % 2 == 0:
        d = d[:-1]
    for idx in range(len(d) - 1, -1, -2):
        for _ in range(int(d[idx])):
            yield last_number
        last_number -= 1

def get_blocks(d):
    blocks = []
    count = 0
    num = 0
    full_lenght = sum(int(x) for i, x in enumerate(d) if i % 2 == 0)
    big_num = big_nums_gen(d)
    for i, char in enumerate(d):
        for _ in range(int(char)):
            if count >= full_lenght:
                return blocks
            if i % 2 == 0:
                blocks.append(num // 2)
            else:
                blocks.append(next(big_num))
            count += 1
        num += 1

blocks = get_blocks(d)
result = 0
for i, n in enumerate(blocks):
    result += i * n
print(result)

c = count()
blocks, slots, waiting = [], [], []

for i, char in enumerate(d):
    repeat = int(char)
    if i % 2 == 0:
        num = next(c)
        blocks.append([num for _ in range(repeat)])
        waiting.append([])
    else:
        slots.append(repeat)

for i in range(len(blocks) - 1, 0, -1):
    size = len(blocks[i])
    for j in range(0, i):
        if slots[j] >= size:
            # print(i, j)
            slots[j] -= size
            waiting[j].append(blocks[i])
            blocks[i] = [None] * size
            break
        
for i in range(len(slots)):
    waiting[i] = sum(waiting[i], []) + ([None] * slots[i])
    
zipped = zip(blocks, waiting)

c = count()
result = 0
for pair in zipped:
    for l in pair:
        for item in l:
            if item is None:
                item = 0
            result += next(c) * item
print(result)
