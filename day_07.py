from operator import mul, add
from itertools import product
from download import data

d = data(7)
equations = []
for l in d.splitlines():
    res, numbers = l.split(":")
    equations.append((int(res), tuple(int(n) for n in numbers.split())))

def make_operations(eq, operators):
    result, numbers = eq
    operations = product(operators, repeat=len(numbers)-1)
    for op in operations:
        n = numbers[0]
        for i in range(len(op)):
            n = op[i](n, numbers[i + 1])
        if result == n:
            return n
    return 0

result = 0
for eq in equations:
    result += make_operations(eq, (add, mul))
print(result)

def concatenation(i, j):
    return int(str(i) + str(j))

result = 0
for eq in equations:
    result += make_operations(eq, (add, mul, concatenation))
print(result)
