from download import data

data = data(2)

data = [[int(n) for n in line.split()] for line in data.splitlines()]

def check_line(l):
    valid_diff = range(1, 4)
    line_sign = None
    for i in range(len(l) - 1):
        diff = l[i + 1] - l[i]
        if diff == 0:
            return 0
        sign = int(diff / abs(diff))
        if line_sign is None:
            line_sign = sign
        elif line_sign != sign:
            return 0
        if abs(diff) not in valid_diff:
            return 0
    return 1

result = 0
for l in data:
    result += check_line(l)
print(result)

def check_line_2(l):
    valid_diff = range(1, 4)
    line_sign = None
    for i in range(len(l) - 1):
        diff = l[i + 1] - l[i]
        if diff == 0:
            return (i, i + 1)
        sign = int(diff / abs(diff))
        if line_sign is None:
            line_sign = sign
        elif line_sign != sign:
            return (i, i + 1)
        if abs(diff) not in valid_diff:
            return (i, i + 1)
    return 1
    
def try_fix(l: list, idxs):
    if idxs == (1, 2):
        first_no_check = check_line_2(l[1:])
        if isinstance(first_no_check, int):
            return 1
    for i in idxs:
        nl = l.copy()
        nl.pop(i)
        res = check_line_2(nl)
        if not isinstance(res, tuple):
            return res
    return 0
    
result = 0
for l in data:
    res = check_line_2(l)
    if not isinstance(res, tuple):
        result += res
    else:
        result += try_fix(l, res)
print(result)
