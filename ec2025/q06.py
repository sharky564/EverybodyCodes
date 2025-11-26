from utils import part1_decorator, part2_decorator, part3_decorator


def process_data(data: list[str]):
    return data[0]

@part1_decorator
def part1(data: list[str]) -> str:
    vals: str = process_data(data)
    total = 0
    masters = {}
    for c in vals:
        if c in 'aA':
            if c.isupper():
                masters[c] = masters.get(c, 0) + 1
            elif c.islower():
                total += masters.get(c.upper(), 0)
    return total
    

@part2_decorator
def part2(data: list[str]) -> str:
    vals: str = process_data(data)
    total = 0
    masters = {}
    for c in vals:
        if c.isupper():
            masters[c] = masters.get(c, 0) + 1
        elif c.islower():
            total += masters.get(c.upper(), 0)
    return total

@part3_decorator
def part3(data: list[str]) -> str:
    vals: str = process_data(data)
    total = 0
    N = 1000
    d = 1000
    l = len(vals)
    masters_prefix = {}
    for i, c in enumerate(vals):
        if c.isupper():
            masters_prefix[c] = masters_prefix.get(c, [0]) + 1
    masters = {}
    for i, c in enumerate(vals):
        if c.isupper():
            masters[c] = masters.get(c, []) + [i]
    print(N, d, l)
    # print(masters)
    for i, c in enumerate(vals):
        if c.islower():
            total += sum((j % l) in masters[c.upper()] for j in range(max(0, i - d), i + d + 1))
            # print(i, c, total)
            total += (N - 2) * sum((j % l) in masters[c.upper()] for j in range(i - d, i + d + 1))
            # print(i, c, total)
            total += sum((j % l) in masters[c.upper()] for j in range(i - d, min(i + d + 1, l)))
            # print(i, c, total)
    return total


if __name__ == '__main__':
    part1()
    part2()
    part3()