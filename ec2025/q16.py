from utils import part1_decorator, part2_decorator, part3_decorator
from math import ceil


def process_data(data: list[str]):
    return [int(x) for x in data[0].split(',')]


@part1_decorator
def part1(data: list[str]) -> str:
    pattern = process_data(data)
    N = 90
    total = 0
    for j in pattern:
        total += N // j
    return total


@part2_decorator
def part2(data: list[str]) -> str:
    walls = process_data(data)
    numbers = []
    for i in range(len(walls)):
        walls[i] -= sum(map(lambda j: (i + 1) % j == 0, numbers))
        if walls[i] != 0:
            numbers.append(i + 1)
    output = 1
    for num in numbers:
        output *= num
    return output
            

@part3_decorator
def part3(data: list[str]) -> str:
    walls = process_data(data)
    numbers = []
    for i in range(len(walls)):
        walls[i] -= sum(map(lambda j: (i + 1) % j == 0, numbers))
        if walls[i] != 0:
            numbers.append(i + 1)
    
    target = 202520252025000
    hi = target
    def calculate(val):
        return sum(map(lambda j: val // j, numbers))
    
    n = calculate(hi)
    x = target / n
    hi *= ceil(x)
    lo = n * int(x)

    if n == target:
        return hi
    while hi - lo > 1:
        mid = (lo + hi) // 2
        x = calculate(mid)
        if x < target:
            lo = mid
        else:
            hi = mid
    if calculate(hi) == target:
        return hi
    return lo


if __name__ == '__main__':
    part1()
    part2()
    part3()