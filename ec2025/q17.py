from utils import part1_decorator, part2_decorator, part3_decorator
import itertools
import heapq


def process_data(data: list[str]):
    return [[int(x) if x.isdigit() else x for x in line.strip()] for line in data]


@part1_decorator
def part1(data: list[str]) -> str:
    grid = process_data(data)
    R = 10
    N = len(grid)
    M = len(grid[0])
    volcano = None
    for i in range(N):
        for j in range(M):
            if grid[i][j] == '@':
                volcano = i, j
                break
        if volcano is not None:
            break
    total = 0
    for i in range(N):
        for j in range(M):
            if (i, j) != volcano and (i - volcano[0])**2 + (j - volcano[1])**2 <= R * R:
                total += grid[i][j]
    return total



@part2_decorator
def part2(data: list[str]) -> str:
    grid = process_data(data)
    N = len(grid)
    M = len(grid[0])
    volcano = None
    for i in range(N):
        for j in range(M):
            if grid[i][j] == '@':
                volcano = i, j
                break
        if volcano is not None:
            break
    max_dest = 0
    max_r = 0
    for r in range(N):
        total = 0
        for i in range(N):
            for j in range(M):
                if (i, j) != volcano and (r - 1) * (r - 1) < (i - volcano[0])**2 + (j - volcano[1])**2 <= r * r:
                    total += grid[i][j]
        if max_dest < total:
            max_dest = total
            max_r = r
    return max_r * max_dest


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

def dijkstra(grid: dict[tuple[int, int], int], start, centre, limit):
    unvisited = set()
    for x, y in grid:
        unvisited.add((x, y, 0))
        unvisited.add((x, y, 1))
    
    distances = {node: float('inf') for node in unvisited}
    new_start = (start[0], start[1], 0)
    new_end = (start[0], start[1], 1)
    distances[new_start] = 0
    queue = PriorityQueue()
    queue.add_task(new_start, 0)
    while True:
        cell = queue.pop_task()
        dist = distances[cell]
        if cell == new_end:
            break
        if dist > limit:
            return float('inf')
        cell_x, cell_y, cell_z = cell
        for dir_x, dir_y in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            adj_cell_x = cell_x + dir_x
            adj_cell_y = cell_y + dir_y
            adj_cell_z = cell_z
            if adj_cell_y < centre[1]:
                if cell_x < centre[0] <= adj_cell_x:
                    adj_cell_z = 1
                elif adj_cell_x < centre[0] <= cell_x:
                    adj_cell_z = 0
            adj_cell = (adj_cell_x, adj_cell_y, adj_cell_z)
            if adj_cell in unvisited:
                distances[adj_cell] = min(distances[adj_cell], dist + grid[(adj_cell[0], adj_cell[1])])
                queue.add_task(adj_cell, distances[adj_cell])
        unvisited.remove(cell)
    return distances[new_end]



@part3_decorator
def part3(data: list[str]) -> str:
    grid = process_data(data)
    N = len(grid)
    M = len(grid[0])
    volcano = None
    start = None
    for i in range(N):
        for j in range(M):
            if grid[i][j] == '@':
                volcano = i, j
            if grid[i][j] == 'S':
                start = i, j
            if volcano is not None and start is not None:
                break
        if volcano is not None and start is not None:
            break
    
    R = 0
    while True:
        volcano_grid = {}
        for i in range(N):
            for j in range(M):
                if (i - volcano[0])**2 + (j - volcano[1])**2 > R * R:
                    volcano_grid[i, j] = grid[i][j]
        volcano_grid[start] = 0
        min_found = dijkstra(volcano_grid, start, volcano, 30 * (R + 1))
        if min_found < 30 * (R + 1):
            return min_found * R
        R += 1


if __name__ == '__main__':
    part1()
    part2()
    part3()