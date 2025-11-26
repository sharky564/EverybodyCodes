from utils import part1_decorator, part2_decorator, part3_decorator
import numba as nb
import numpy as np

def process_data(data: list[str]):
    num = tuple(map(int, data[0][:-1].split('[')[1].split(',')))
    return num


def run_point_process(px, py):
    x, y = 0, 0
    for _ in range(3):
        new_x = x * x - y * y
        new_y = 2 * x * y

        if new_x >= 0:
            new_x = new_x // 10
        else:
            new_x = -(-new_x // 10)
        if new_y >= 0:
            new_y = new_y // 10
        else:
            new_y = -(-new_y // 10)
        
        x = new_x + px
        y = new_y + py
    return x, y


@nb.jit()
def check_point_process(px, py):
    x, y = 0, 0
    for _ in range(100):
        new_x = x * x - y * y
        new_y = 2 * x * y

        if new_x >= 0:
            new_x = new_x // 100_000
        else:
            new_x = -(-new_x // 100_000)
        if new_y >= 0:
            new_y = new_y // 100_000
        else:
            new_y = -(-new_y // 100_000)
        
        x = new_x + px
        y = new_y + py

        if abs(x) > 1_000_000 or abs(y) > 1_000_000:
            return False
    return True

@nb.njit(parallel=True)
def check_grid(points_x, points_y):
    n = len(points_x)
    results = np.zeros(n, dtype=np.bool)
    for i in range(n):
        results[i] = check_point_process(points_x[i], points_y[i])
    return np.count_nonzero(results)

@part1_decorator
def part1(data: list[str]) -> str:
    px, py = process_data(data)
    x, y = run_point_process(px, py)
    return f'[{x},{y}]'
    


@part2_decorator
def part2(data: list[str]) -> str:
    px, py = process_data(data)
    points = [(i, j) for i in range(px, px + 1010, 10) for j in range(py, py + 1010, 10)]
    points_x, points_y = map(list, zip(*points))

    return check_grid(points_x, points_y)

    

@part3_decorator
def part3(data: list[str]) -> str:
    px, py = process_data(data)
    points = [(i, j) for i in range(px, px + 1001) for j in range(py, py + 1001)]
    points_x, points_y = map(list, zip(*points))

    return check_grid(points_x, points_y)


if __name__ == '__main__':
    part1()
    part2()
    part3()