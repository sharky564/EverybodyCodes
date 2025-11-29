import heapq
import math
from utils import part1_decorator, part2_decorator, part3_decorator

def process_data(data: list[str]):
    return [[int(x) if x.isdigit() else x for x in line.strip()] for line in data]

def find_locations(grid):
    volcano, start = None, None
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == '@':
                volcano = (r, c)
            elif val == 'S':
                start = (r, c)
    return volcano, start

def get_power_value(val: int | str):
    return val if isinstance(val, int) else 0

@part1_decorator
def part1(data: list[str]):
    grid = process_data(data)
    volcano, _ = find_locations(grid)
    if not volcano:
        return 0

    vr, vc = volcano
    radius = 10
    total = 0
    rows, cols = len(grid), len(grid[0])

    r_min = max(0, vr - radius)
    r_max = min(rows, vr + radius + 1)
    
    for r in range(r_min, r_max):
        for c in range(cols): 
            if (r - vr)**2 + (c - vc)**2 <= radius**2:
                if (r, c) != volcano:
                    total += get_power_value(grid[r][c])
    return total

@part2_decorator
def part2(data: list[str]) -> int:
    grid = process_data(data)
    volcano, _ = find_locations(grid)
    if not volcano:
        return 0

    vr, vc = volcano
    radius_sums = {}
    
    rows = len(grid)
    cols = len(grid[0])

    for r in range(rows):
        for c in range(cols):
            if (r, c) == volcano:
                continue
            
            val = get_power_value(grid[r][c])
            if val == 0:
                continue

            dist_sq = (r - vr)**2 + (c - vc)**2
            dist = math.sqrt(dist_sq)
            ring_radius = math.ceil(dist)
            
            radius_sums[ring_radius] = radius_sums.get(ring_radius, 0) + val

    max_r, max_val = max(radius_sums.items(), key=lambda t: t[1])
            
    return max_r * max_val

def solve_dijkstra(grid, start, volcano, min_radius):
    rows, cols = len(grid), len(grid[0])
    vr, vc = volcano
    pq = [(0, start[0], start[1], 0)]
    min_costs = {} 
    min_costs[(start[0], start[1], 0)] = 0
    
    limit_sq = min_radius * min_radius
    cost_limit = 30 * (min_radius + 1)

    while pq:
        cost, r, c, phase = heapq.heappop(pq)

        if cost > cost_limit:
            return float('inf')
        if (r, c, phase) == (start[0], start[1], 1):
            return cost
        if cost > min_costs.get((r, c, phase), float('inf')):
            continue

        for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            n_phase = phase
            if nc < vc:
                if r < vr <= nr:
                    n_phase = 1
                elif nr < vr <= r:
                    n_phase = 0
            if (nr - vr)**2 + (nc - vc)**2 <= limit_sq:
                continue

            val = get_power_value(grid[nr][nc])
            new_cost = cost + val
            state = (nr, nc, n_phase)
            if new_cost < min_costs.get(state, float('inf')):
                min_costs[state] = new_cost
                heapq.heappush(pq, (new_cost, nr, nc, n_phase))

    return float('inf')

@part3_decorator
def part3(data: list[str]) -> int:
    grid = process_data(data)
    volcano, start = find_locations(grid)
    R = 0
    while True:
        min_found = solve_dijkstra(grid, start, volcano, R)
        if min_found < 30 * (R + 1):
            return min_found * R
        R += 1

if __name__ == '__main__':
    part1()
    part2()
    part3()