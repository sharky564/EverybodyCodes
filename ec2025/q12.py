from utils import part1_decorator, part2_decorator, part3_decorator

def process_data(data: list[str]):
    arr = [list(map(int, line.strip())) for line in data]
    out = {}
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            out[i, j] = arr[i][j]
    return arr, out


@part1_decorator
def part1(data: list[str]) -> str:
    grid, arr = process_data(data)
    seen = {(0, 0)}
    queue = [(0, 0)]
    count = 1
    while queue:
        cell = queue.pop()
        cell_x, cell_y = cell
        for dir_x, dir_y in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_cell = (cell_x + dir_x, cell_y + dir_y)
            if new_cell in arr and arr[new_cell] <= arr[cell] and new_cell not in seen:
                seen.add(new_cell)
                queue.append(new_cell)
                count += 1
    return count


@part2_decorator
def part2(data: list[str]) -> str:
    grid, arr = process_data(data)
    N = len(grid)
    M = len(grid[0])
    seen = {(0, 0), (N-1, M-1)}
    queue = [(0, 0), (N-1, M-1)]
    count = len(seen)
    while queue:
        cell = queue.pop()
        cell_x, cell_y = cell
        for dir_x, dir_y in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_cell = (cell_x + dir_x, cell_y + dir_y)
            if new_cell in arr and arr[new_cell] <= arr[cell] and new_cell not in seen:
                seen.add(new_cell)
                queue.append(new_cell)
                count += 1
    return count

def ignite(init_cell, arr, ig):
    seen = {init_cell}.union(ig)
    queue = [init_cell]
    count = 1
    while queue:
        cell = queue.pop()
        cell_x, cell_y = cell
        for dir_x, dir_y in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_cell = (cell_x + dir_x, cell_y + dir_y)
            if new_cell in arr and arr[new_cell] <= arr[cell] and new_cell not in seen:
                seen.add(new_cell)
                queue.append(new_cell)
                count += 1
    return count, seen


@part3_decorator
def part3(data: list[str]) -> str:
    grid, arr = process_data(data)
    max_seen = set()
    total = 0
    for i in range(3):
        max_found = 0
        max_cell = None
        curr_max_seen = set()
        for cell in filter(lambda t: t not in max_seen, arr):
            count, seen = ignite(cell, arr, max_seen)
            if count > max_found:
                max_found = count
                max_cell = cell
                curr_max_seen = seen
        print(i, max_cell, max_found)
        max_seen = curr_max_seen
        total += max_found
    return total


if __name__ == '__main__':
    part1()
    part2()
    part3()