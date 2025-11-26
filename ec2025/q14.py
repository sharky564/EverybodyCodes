from utils import part1_decorator, part2_decorator, part3_decorator

def process_data(data: list[str]):
    return [list(line.strip()) for line in data]

def evolve(grid_dict, active_neighbours):
    new_grid_dict = dict(grid_dict)
    new_active_neighbours = dict(active_neighbours)
    for i, j in grid_dict:
        if grid_dict[i, j] == '#' and active_neighbours[i, j] % 2 == 0:
            new_grid_dict[i, j] = '.'
            for dir_x, dir_y in [(-1, -1), (-1, 1), (1, 1), (1, -1)]:
                adj_cell = i + dir_x, j + dir_y
                if adj_cell in grid_dict:
                    new_active_neighbours[adj_cell] -= 1
        elif grid_dict[i, j] == '.' and active_neighbours[i, j] % 2 == 0:
            new_grid_dict[i, j] = '#'
            for dir_x, dir_y in [(-1, -1), (-1, 1), (1, 1), (1, -1)]:
                adj_cell = i + dir_x, j + dir_y
                if adj_cell in grid_dict:
                    new_active_neighbours[adj_cell] += 1
    return new_grid_dict, new_active_neighbours

def display_grid(grid_dict):
    output = ''
    N = max(i for i, j in grid_dict)
    M = max(j for i, j in grid_dict)
    for i in range(N + 1):
        for j in range(M + 1):
            output += str(grid_dict[i, j])
        output += '\n'
    return output


@part1_decorator
def part1(data: list[str]) -> str:
    grid = process_data(data)
    grid_dict = {}
    active_neighbours = {}
    N = len(grid)
    M = len(grid[0])
    for i in range(N):
        for j in range(M):
            grid_dict[i, j] = grid[i][j]
            active_neighbours[i, j] = 0
    for i in range(N):
        for j in range(M):
            if grid_dict[i, j] == '#':
                for dir_x, dir_y in [(-1, -1), (-1, 1), (1, 1), (1, -1)]:
                    adj_cell = i + dir_x, j + dir_y
                    if adj_cell in grid_dict:
                        active_neighbours[adj_cell] += 1

    # print(display_grid(grid_dict))
    # print(display_grid(active_neighbours))
    total = 0
    for r in range(10):
        grid_dict, active_neighbours = evolve(grid_dict, active_neighbours)
        active = len(list(filter(lambda t: t == '#', grid_dict.values())))
        total += active
        # print(r, active)
        # print(display_grid(grid_dict))
        # print(display_grid(active_neighbours))

    return total

    
@part2_decorator
def part2(data: list[str]) -> str:
    grid = process_data(data)
    grid_dict = {}
    active_neighbours = {}
    N = len(grid)
    M = len(grid[0])
    for i in range(N):
        for j in range(M):
            grid_dict[i, j] = grid[i][j]
            active_neighbours[i, j] = 0
    for i in range(N):
        for j in range(M):
            if grid_dict[i, j] == '#':
                for dir_x, dir_y in [(-1, -1), (-1, 1), (1, 1), (1, -1)]:
                    adj_cell = i + dir_x, j + dir_y
                    if adj_cell in grid_dict:
                        active_neighbours[adj_cell] += 1
    total = 0
    for r in range(2025):
        grid_dict, active_neighbours = evolve(grid_dict, active_neighbours)
        active = len(list(filter(lambda t: t == '#', grid_dict.values())))
        total += active

    return total


def match_middle(grid_dict, middle_grid_dict):
    return all(middle_grid_dict[x] == grid_dict[x] for x in middle_grid_dict)


@part3_decorator
def part3(data: list[str]) -> str:
    grid = [['.' for _ in range(34)] for _ in range(34)]
    grid_dict = {}
    active_neighbours = {}
    D = 34
    for i in range(D):
        for j in range(D):
            grid_dict[i, j] = grid[i][j]
            active_neighbours[i, j] = 0
    for i in range(D):
        for j in range(D):
            if grid_dict[i, j] == '#':
                for dir_x, dir_y in [(-1, -1), (-1, 1), (1, 1), (1, -1)]:
                    adj_cell = i + dir_x, j + dir_y
                    if adj_cell in grid_dict:
                        active_neighbours[adj_cell] += 1
    
    middle_grid = process_data(data)
    N = len(middle_grid)
    M = len(middle_grid[0])
    middle_grid_dict = {}
    for i in range(N):
        for j in range(M):
            middle_grid_dict[(D - N) // 2 + i, (D - M) // 2 + j] = middle_grid[i][j]
    
    count = 0
    known = {hash(display_grid(grid_dict)): count}
    sequence = [grid_dict]
    while True:
        grid_dict, active_neighbours = evolve(grid_dict, active_neighbours)
        grid_hash = hash(display_grid(grid_dict))
        if grid_hash not in known:
            count += 1
            known[grid_hash] = count
            sequence.append(grid_dict)
        else:
            break
    
    N = 1000000000
    start = known[hash(display_grid(grid_dict))]
    length = len(sequence) - start
    total = 0
    num_loops, num_left = divmod(N - start, length)

    for i in range(start, len(sequence)):
        if match_middle(sequence[i], middle_grid_dict):
            num_active = len(list(filter(lambda t: t == '#', sequence[i].values())))
            total += num_active
    total *= num_loops
    
    for i in range(start):
        if match_middle(sequence[i], middle_grid_dict):
            num_active = len(list(filter(lambda t: t == '#', sequence[i].values())))
            total += num_active
    
    
    for i in range(start, start + num_left):
        if match_middle(sequence[i], middle_grid_dict):
            num_active = len(list(filter(lambda t: t == '#', sequence[i].values())))
            total += num_active

    return total


if __name__ == '__main__':
    part1()
    part2()
    part3()