from download import data
import re

word = "XMAS"
xmas = re.compile(word)
inpt = [[l for l in line] for line in data(4).splitlines()]

def transpose(matrix):
    size = len(matrix)
    return [[matrix[j][i] for j in range(size)] for i in range(size)]

def skew(matrix):
    lw = len(word)
    size = len(matrix)
    new = []
    for i in range(lw, size + 1):
        idxs = zip(range(i), reversed(range(i)))
        new.append([matrix[i][j] for i, j in idxs])
    for i in range(1, size - lw + 1):
        idxs = zip(range(i, size - 1 + 1), reversed(range(i, size - 1 + 1)))
        new.append([matrix[i][j] for i, j in idxs])
    return new

def count_word(lines):
    c = 0
    for line in lines:
        for direction in ("".join(line), "".join(reversed(line))):
            c += len(xmas.findall(direction))
    return c

transformations = inpt, transpose(inpt), skew(inpt), skew(list(reversed(inpt)))

result = 0
for trans in transformations:
    result += count_word(trans)
print(result)

def get_neighbours(idxs):
    i, j = idxs
    return ((i - 1, j - 1), (i - 1, j + 1)), ((i + 1, j - 1), (i + 1, j + 1))

result = 0
for figure in (inpt, transpose(inpt)):
    size = len(figure)
    for pair in [(i, j) for i in range(1, size - 1) for j in range(1, size -1)]:
        if figure[pair[0]][pair[1]] != 'A':
            continue
        (ul, ur), (ll, lr) = get_neighbours(pair)
        upper = figure[ul[0]][ul[1]], figure[ur[0]][ur[1]]
        lower = figure[ll[0]][ll[1]], figure[lr[0]][lr[1]]
        w = (set(upper), set(lower))
        if w in (({'M'}, {'S'}), ({'S'}, {'M'})):
            result += 1
print(result)