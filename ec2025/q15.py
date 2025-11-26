from utils import part1_decorator, part2_decorator, part3_decorator
import itertools
import heapq


def process_data(data: list[str]):
    return [(s[0], int(s[1:])) for s in data[0].strip().split(',')]

class PriorityQueue():
    def __init__(self):
        self.pq = []
        self.entry_finder = {}
        self.REMOVED = '<removed-task>'
        self.counter = itertools.count()

    def add_task(self, task, priority=0):
        if task in self.entry_finder:
            self.remove_task(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heapq.heappush(self.pq, entry)

    def remove_task(self, task):
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED

    def pop_task(self):
        while self.pq:
            priority, count, task = heapq.heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return task
        raise KeyError('pop from an empty priority queue')


def display_grid(N, A, B, C, D, S, E, walls, distances):
    new_grid = [[((N - 1) // 2 * ' ' + '.'  + -((1 - N) // 2) * ' ') for _ in range(D - C + 1)] for _ in range(B - A + 1)]
    for cell, dist in distances.items():
        x = str(dist)
        t = len(x)
        x += (N - t) // 2 * ' '
        while len(x) < N:
            x = ' ' + x
        new_grid[cell[0] - A][cell[1] - C] = x
    new_grid[S[0] - A][S[1] - C] = (N - 1) // 2 * ' ' + 'S' + -((1 - N) // 2) * ' '
    new_grid[E[0] - A][E[1] - C] = (N - 1) // 2 * ' ' + 'E' + -((1 - N) // 2) * ' '
    for w in walls:
        new_grid[w[0] - A][w[1] - C] = (N - 1) // 2 * ' ' + '#' + -((1 - N) // 2) * ' '
    return '\n'.join(''.join(s) for s in new_grid)

def display_path(A, B, C, D, S, E, walls, path):
    new_grid = [['.' for _ in range(D - C + 1)] for _ in range(B - A + 1)]
    for cell in path:
        new_grid[cell[0] - A][cell[1] - C] = 'X'
    new_grid[S[0] - A][S[1] - C] = 'S'
    new_grid[E[0] - A][E[1] - C] = 'E'
    for w in walls:
        new_grid[w[0] - A][w[1] - C] = '#'
    return '\n'.join(''.join(s) for s in new_grid)


def least_insert_index(sorted_arr, val):
    if val <= sorted_arr[0]:
        return 0
    if val > sorted_arr[-1]:
        return len(sorted_arr)
    elif val == sorted_arr[-1]:
        return len(sorted_arr) - 1
    lo = 0
    hi = len(sorted_arr)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if val == sorted_arr[mid]:
            return mid
        elif val > sorted_arr[mid]:
            lo = mid
        else:
            hi = mid
    return hi


@part1_decorator
def part1(data: list[str]) -> str:
    walls = process_data(data)
    curr_x, curr_y = (0, 0)
    nodes = [(curr_x, curr_y)]
    dir_x, dir_y = -1, 0
    for direction, length in walls:
        if direction == 'L':
            dir_x, dir_y,  = -dir_y, dir_x
        else:
            dir_x, dir_y,  = dir_y, -dir_x
        curr_x += length * dir_x
        curr_y += length * dir_y
        nodes.append((curr_x, curr_y))
    S = nodes[0]
    E = nodes[-1]
    valid_x = sorted({S[0], E[0]}.union(*[[i - 1, i + 1] for i, j in nodes]))
    valid_y = sorted({S[1], E[1]}.union(*[[j - 1, j + 1] for i, j in nodes]))

    translated_start = (valid_x.index(S[0]), valid_y.index(S[1]))
    translated_end = (valid_x.index(E[0]), valid_y.index(E[1]))
    wall_nodes = set()
    for wall_node1, wall_node2 in zip(nodes, nodes[1:]):
        (x1, y1), (x2, y2) = wall_node1, wall_node2
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        x_i, x_j = least_insert_index(valid_x, x1), least_insert_index(valid_x, x2)
        y_i, y_j = least_insert_index(valid_y, y1), least_insert_index(valid_y, y2)        
        if x1 == x2:
            for y in range(y_i, y_j):
                wall_nodes.add((valid_x[x_i], valid_y[y]))
        else:
            for x in range(x_i, x_j):
                wall_nodes.add((valid_x[x], valid_y[y_i]))
    if translated_start in wall_nodes:
        wall_nodes.remove(translated_start)
    if translated_end in wall_nodes:
        wall_nodes.remove(translated_end)
    
    distances = {translated_start: 0}
    visited = set()
    queue = PriorityQueue()
    queue.add_task(translated_start, (0, abs(E[0] - S[0]) + abs(E[1] - S[1])))
    while True:
        cell = queue.pop_task()
        dist = distances[cell]
        if cell == translated_end:
            break
        cell_x, cell_y = cell
        for dir_x, dir_y in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            adj_cell_x = cell_x + dir_x
            adj_cell_y = cell_y + dir_y
            if 0 <= adj_cell_x < len(valid_x) and 0 <= adj_cell_y < len(valid_y):
                length = abs(valid_x[adj_cell_x] - valid_x[cell_x]) + abs(valid_y[adj_cell_y] - valid_y[cell_y])
                if length != 2 or ((valid_x[cell_x] + valid_x[adj_cell_x]) // 2, (valid_y[cell_y] + valid_y[adj_cell_y]) // 2) not in wall_nodes:
                    adj_cell = (adj_cell_x, adj_cell_y)
                    if adj_cell not in visited:
                        distances[adj_cell] = min(distances.get(adj_cell, float('inf')), dist + length)
                        queue.add_task(adj_cell, (distances[adj_cell], abs(E[0] - valid_x[adj_cell_x]) + abs(E[1] - valid_y[adj_cell_y])))
            visited.add(cell)
    return distances[translated_end]



@part2_decorator
def part2(data: list[str]) -> str:
    walls = process_data(data)
    curr_x, curr_y = (0, 0)
    nodes = [(curr_x, curr_y)]
    dir_x, dir_y = -1, 0
    for direction, length in walls:
        if direction == 'L':
            dir_x, dir_y,  = -dir_y, dir_x
        else:
            dir_x, dir_y,  = dir_y, -dir_x
        curr_x += length * dir_x
        curr_y += length * dir_y
        nodes.append((curr_x, curr_y))
    S = nodes[0]
    E = nodes[-1]
    valid_x = sorted(set().union(*[[i - 1, i, i + 1] for i, j in nodes]))
    valid_y = sorted(set().union(*[[j - 1, j, j + 1] for i, j in nodes]))

    wall_nodes = []
    for wall_node1, wall_node2 in zip(nodes, nodes[1:]):
        x_i, x_j = sorted([valid_x.index(wall_node1[0]), valid_x.index(wall_node2[0])])
        y_i, y_j = sorted([valid_y.index(wall_node1[1]), valid_y.index(wall_node2[1])])
        if x_i == x_j:
            for y in range(y_i, y_j + 1):
                wall_nodes.append((valid_x[x_i], valid_y[y]))
        else:
            for x in range(x_i, x_j + 1):
                wall_nodes.append((valid_x[x], valid_y[y_i]))
    wall_nodes.remove(S)
    wall_nodes.remove(E)

    pq = []
    entry_finder = {}
    REMOVED = '<removed-task>'
    counter = itertools.count()

    def add_task(task, priority=0):
        'Add a new task or update the priority of an existing task'
        if task in entry_finder:
            remove_task(task)
        count = next(counter)
        entry = [priority, count, task]
        entry_finder[task] = entry
        heapq.heappush(pq, entry)

    def remove_task(task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = entry_finder.pop(task)
        entry[-1] = REMOVED

    def pop_task():
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while pq:
            priority, count, task = heapq.heappop(pq)
            if task is not REMOVED:
                del entry_finder[task]
                return task
        raise KeyError('pop from an empty priority queue')

    translated_start = (valid_x.index(S[0]), valid_y.index(S[1]))
    translated_end = (valid_x.index(E[0]), valid_y.index(E[1]))
    distances = {translated_start: 0}
    visited = set()
    add_task(translated_start, (0, abs(E[0] - S[0]) + abs(E[1] - S[1])))
    while True:
        cell = pop_task()
        dist = distances[cell]
        # print(dist, cell)
        if cell == translated_end:
            break
        cell_x, cell_y = cell
        for dir_x, dir_y in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            adj_cell_x = cell_x + dir_x
            adj_cell_y = cell_y + dir_y
            length = abs(valid_x[adj_cell_x] - valid_x[cell_x]) + abs(valid_y[adj_cell_y] - valid_y[cell_y])
            adj_cell = (adj_cell_x, adj_cell_y)
            untranslated_adj_cell = (valid_x[adj_cell_x], valid_y[adj_cell_y])
            if adj_cell not in visited and untranslated_adj_cell not in wall_nodes:
                distances[adj_cell] = min(distances.get(adj_cell, float('inf')), dist + length)
                add_task(adj_cell, (distances[adj_cell], abs(E[0] - untranslated_adj_cell[0]) + abs(E[1] - untranslated_adj_cell[1])))
            visited.add(cell)
    return distances[translated_end]


@part3_decorator
def part3(data: list[str]) -> str:
    walls = process_data(data)
    curr_x, curr_y = (0, 0)
    nodes = [(curr_x, curr_y)]
    dir_x, dir_y = -1, 0
    for direction, length in walls:
        if direction == 'L':
            dir_x, dir_y,  = -dir_y, dir_x
        else:
            dir_x, dir_y,  = dir_y, -dir_x
        curr_x += length * dir_x
        curr_y += length * dir_y
        nodes.append((curr_x, curr_y))
    S = nodes[0]
    E = nodes[-1]
    valid_x = sorted(set().union(*[[i - 1, i, i + 1] for i, j in nodes]))
    valid_y = sorted(set().union(*[[j - 1, j, j + 1] for i, j in nodes]))

    wall_nodes = []
    for wall_node1, wall_node2 in zip(nodes, nodes[1:]):
        x_i, x_j = sorted([valid_x.index(wall_node1[0]), valid_x.index(wall_node2[0])])
        y_i, y_j = sorted([valid_y.index(wall_node1[1]), valid_y.index(wall_node2[1])])
        if x_i == x_j:
            for y in range(y_i, y_j + 1):
                wall_nodes.append((valid_x[x_i], valid_y[y]))
        else:
            for x in range(x_i, x_j + 1):
                wall_nodes.append((valid_x[x], valid_y[y_i]))
    wall_nodes.remove(S)
    wall_nodes.remove(E)

    pq = []
    entry_finder = {}
    REMOVED = '<removed-task>'
    counter = itertools.count()

    def add_task(task, priority=0):
        'Add a new task or update the priority of an existing task'
        if task in entry_finder:
            remove_task(task)
        count = next(counter)
        entry = [priority, count, task]
        entry_finder[task] = entry
        heapq.heappush(pq, entry)

    def remove_task(task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = entry_finder.pop(task)
        entry[-1] = REMOVED

    def pop_task():
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while pq:
            priority, count, task = heapq.heappop(pq)
            if task is not REMOVED:
                del entry_finder[task]
                return task
        raise KeyError('pop from an empty priority queue')

    translated_start = (valid_x.index(S[0]), valid_y.index(S[1]))
    translated_end = (valid_x.index(E[0]), valid_y.index(E[1]))
    distances = {translated_start: 0}
    visited = set()
    add_task(translated_start, (0, abs(E[0] - S[0]) + abs(E[1] - S[1])))
    while True:
        cell = pop_task()
        dist = distances[cell]
        # print(dist, cell)
        if cell == translated_end:
            break
        cell_x, cell_y = cell
        for dir_x, dir_y in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            adj_cell_x = cell_x + dir_x
            adj_cell_y = cell_y + dir_y
            length = abs(valid_x[adj_cell_x] - valid_x[cell_x]) + abs(valid_y[adj_cell_y] - valid_y[cell_y])
            adj_cell = (adj_cell_x, adj_cell_y)
            untranslated_adj_cell = (valid_x[adj_cell_x], valid_y[adj_cell_y])
            if adj_cell not in visited and untranslated_adj_cell not in wall_nodes:
                distances[adj_cell] = min(distances.get(adj_cell, float('inf')), dist + length)
                add_task(adj_cell, (distances[adj_cell], abs(E[0] - untranslated_adj_cell[0]) + abs(E[1] - untranslated_adj_cell[1])))
            visited.add(cell)
    return distances[translated_end]


if __name__ == '__main__':
    part1()
    # part2()
    # part3()