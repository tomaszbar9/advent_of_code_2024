from itertools import cycle
from collections import defaultdict
from download import data

d = data(6)
d = d.splitlines()
obstacles = set()
for i, line in enumerate(d):
    for j, ch in enumerate(line):
        if ch == "#":
            obstacles.add((i, j))
        elif ch == "^":
            start = i, j

position = start
visited = set()
size = len(d)
assert len(d) == len(d[0])
directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
direction_indices = cycle(range(4))
cur_dir_idx = next(direction_indices)

def check_path(p, dir_idx, obstacles=obstacles):
    d = directions[dir_idx]
    passive_idx, active_idx = int(d[1] == 0), int(d[0] == 0)
    active_direction = p[active_idx], d[active_idx]
    if (x:=active_direction[1]) == 1:
        end = size
    else:
        end = x
    temp = [0, 0]
    temp[passive_idx] = p[passive_idx]
    vis = []
    for step in range(active_direction[0], end, active_direction[1]):
        temp[active_idx] = step
        cur_pos = tuple(temp)
        if cur_pos in obstacles:
            return True, vis
        vis.append(cur_pos)
        if any(i in (0, size-1) for i in cur_pos):
            return False, vis

def check_3_turns(position, cdi):
    d_indices = [(cdi + i) % 4 for i in range(1, 4)]
    for idx in d_indices:
        inside, path = check_path(position, idx)
        if not inside:
            return False
        position = path[-1]
    return True

def look_for_loop(obstacles):
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    direction_indices = cycle(range(4))
    cur_dir_idx = next(direction_indices)
    visited = defaultdict(set)
    position = start
    inside = True
    while inside:
        inside, path = check_path(position, cur_dir_idx, obstacles)
        position = path[-1]
        if position in visited[cur_dir_idx]:
            return 1
        visited[cur_dir_idx].add(position)
        cur_dir_idx = next(direction_indices)
    return 0

inside = True
while inside:
    inside, path = check_path(position, cur_dir_idx)
    visited.update(set(path))
    position = path[-1]
    cur_dir_idx = next(direction_indices)
print(len(visited))

position = start
visited = set()
virtual_obstacles = set()
direction_indices = cycle(range(4))
cur_dir_idx = next(direction_indices)
inside = True
while inside:
    inside, path = check_path(position, cur_dir_idx)
    for position in path:
        direction = directions[cur_dir_idx]
        virtual_obstacle = position[0] + direction[0], position[1] + direction[1]
        if virtual_obstacle not in visited:
            if check_3_turns(position, cur_dir_idx):
                virtual_obstacles.add(virtual_obstacle)
    visited.update(set(path))
    position = path[-1]
    cur_dir_idx = next(direction_indices)
result = 0
for vob in virtual_obstacles:
    result += look_for_loop(obstacles | {vob})
print(result)
