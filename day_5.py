from download import data
from collections import defaultdict

d = data(5)
rules, updates = d.split("\n\n")

rules = set(tuple(int(x) for x in line.split("|")) for line in rules.splitlines())
updates = [[int(x) for x in line.split(",")] for line in updates.splitlines()]

def check_update(update):
    gen = ((e, update[j]) for i, e in enumerate(update) for j in range(i + 1, len(update)))
    for pair in gen:
        if pair not in rules:
            return 0
    return update[len(update) // 2]
    
result = 0
for u in updates:
    result += check_update(u)
print(result)

rules_dict = defaultdict(set)
for rule in rules:
    rules_dict[rule[0]].add(rule[1])


class Number:
    def __init__(self, value):
        self.value = value

    def __lt__(self, x):
        return self.value in rules_dict[x.value]

    def __repr__(self):
        return str(self.value)


def correct_update(update):
    gen = ((e, update[j]) for i, e in enumerate(update) for j in range(i + 1, len(update)))
    if all(pair in rules for pair in gen):
        return 0
    numbers = sorted([Number(x) for x in update], reverse=True)
    return numbers[len(numbers) // 2].value
    
result = 0
for u in updates:
    result += correct_update(u)
print(result)
