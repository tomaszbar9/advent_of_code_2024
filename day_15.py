import re
from copy import deepcopy
from download import data

puzzle_input = data(15)

def turn_right(board):
    new_board = [[board[i][j] for i in range(len(board) -1, -1, -1)] for j in range(len(board[0]))]
    for i, row in enumerate(new_board):
        new_board[i] = "".join(row)
        if "@" in new_board[i]:
            robot = i, new_board[i].index("@")
    return new_board, robot

def move(board, robot):
    row = board[robot[0]]
    left_side, right_side = row.split("@")
    if right_side[0] == '.':
        board[robot[0]] = left_side + ".@" + right_side[1:]
    else:
        m = re.match(r'O+', right_side)
        if m and right_side[m.end()] == '.':
            board[robot[0]] = left_side + ".@" + m.group() + right_side[m.end() + 1:]

def back_to_original_position(board, curr):
    b = deepcopy(board)
    diff = -curr + 4
    for turn in range(diff):
        b, robot = turn_right(b)
    return b

def count_boxes(board):
    count = 0
    for i in range(1, len(board)):
        for j, f in enumerate(board[i]):
            if f == "O":
                count += 100 * i + j
    return count

board, instructions = puzzle_input.split('\n\n')
board = board.splitlines()
instructions = ''.join(instructions.splitlines())
instructions = (int(i) for i in instructions.translate(str.maketrans(">^<v", "0123")))

curr = 0
for i in instructions:
    diff = i - curr
    if diff < 0:
        diff += 4
    for turn in range(diff):
        board, robot = turn_right(board)
    move(board, robot)
    curr = i

print(count_boxes(back_to_original_position(board, i)))

def double_board(board):
    new = []
    walls, boxes = [], []
    for i, line in enumerate(board.splitlines()):
        wall, box = set(), set()
        walls.append(wall)
        boxes.append(box)
        count = 0
        for j, char in enumerate(line):
            match char:
                case "#":
                    wall.update({count, count + 1})
                case "O":
                    box.add(count)
                case "@":
                    robot = i, count
            count += 2
    return walls, boxes, robot

def print_board(walls, boxes, robot):
    box = False
    witdth = len(walls[0])
    for i, w in enumerate(walls):
        b = boxes[i]
        for j in range(witdth):
            if box:
                box = False
                continue
            elif j in w:
                print("#", end="")
            elif j in b:
                print("[]", end="")
                box = True
            elif (i, j) == robot:
                print("@", end="")
            else:
                print(".", end="")
        print()

def move_up(robot):
    i, j = robot
    up = i - 1
    if j in walls[up]:
        return robot
    way_open = False
    boxes_above = boxes[up] & {j - 1, j}
    if not boxes_above:
        return up, j
    boxes_to_move = set((up, idx) for idx in boxes_above)
    while boxes_above:
        up -= 1
        new_row_boxes = set()
        for box in boxes_above:
            full_box = {box, box + 1}
            if full_box & walls[up]:
                return robot
            new_row_boxes |= set(b for b in boxes[up] if {b, b + 1} & full_box)
        boxes_above = new_row_boxes
        boxes_to_move |= set((up, idx) for idx in boxes_above)
    for row, idx in sorted(boxes_to_move, key=lambda x: x[0]):
        boxes[row].remove(idx)
        boxes[row - 1].add(idx)
    return robot[0] - 1, robot[1]

def move_horizontaly(robot, right=True):
    if right:
        step = 1
    else:
        step = -1
    row, idx = robot
    if (idx + step) in walls[row]:
        return robot
    full_boxes = boxes[row] | {b + 1 for b in boxes[row]}
    if (idx + step) not in full_boxes:
        return row, idx + step
    steps = step
    boxes_to_move = set()
    while (cur_pos := idx + steps) in full_boxes:
        boxes_to_move.add(cur_pos)
        steps += step
    if cur_pos in walls[row]:
        return robot
    full_boxes -= boxes_to_move
    boxes_to_move = {b + step for b in boxes_to_move}
    boxes[row] = set(sorted(full_boxes | boxes_to_move)[::2])
    return row, idx + step

def count_boxes(boxes):
    result = 0
    for i, row in enumerate(boxes):
        for j in row:
            result += 100 * i + j
    return result

board, instructions = puzzle_input.split('\n\n')
instructions = ''.join(instructions.splitlines())
walls, boxes, robot = double_board(board)

for inst in instructions:
    # print("move:", inst)
    match inst:
        case ">":
            robot = move_horizontaly(robot)
        case "<":
            robot = move_horizontaly(robot, right=False)
        case "^":
            robot = move_up(robot)
        case "v":
            robot = len(walls) - 1 - robot[0], robot[1]
            walls, boxes = list(reversed(walls)), list(reversed(boxes))
            robot = move_up(robot)
            robot = len(walls) - 1 - robot[0], robot[1]
            walls, boxes = list(reversed(walls)), list(reversed(boxes))

print(count_boxes(boxes))
