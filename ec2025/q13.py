from utils import part1_decorator, part2_decorator, part3_decorator

def process_data(data: list[str]):
    return [int(line) for line in data]

def process_data2(data: list[str]):
    output = []
    for line in data:
        x, y = line.split('-')
        output.append(range(int(x), int(y) + 1))
    return output

@part1_decorator
def part1(data: list[str]) -> str:
    arr = process_data(data)
    N = len(arr) + 1
    clock = [1 for _ in range(N)]
    for i, val in enumerate(arr, 1):
        j = i % 2 * i - i // 2
        clock[j] = val
    return clock[2025 % N]


@part2_decorator
def part2(data: list[str]) -> str:
    arr = process_data2(data)
    N = len(arr) + 1
    clock = [range(1, 2) for _ in range(N)]
    for i, val in enumerate(arr, 1):
        j = i % 2 * i - i // 2
        if j < 0:
            clock[j] = val[::-1]
        else:
            clock[j] = val

    M = 0
    indices = []
    for r in clock:
        indices.append(M)
        M += len(r)
    T = 20252025 % M
    for (i, t) in enumerate(indices):
        if T < t:
            break
    S = T - indices[i - 1]
    return clock[i - 1][S]


@part3_decorator
def part3(data: list[str]) -> str:
    arr = process_data2(data)
    print(range(0, 2)[::-1])
    N = len(arr) + 1
    clock = [range(1, 2) for _ in range(N)]
    for i, val in enumerate(arr, 1):
        j = i % 2 * i - i // 2
        if j < 0:
            clock[j] = val[::-1]
        else:
            clock[j] = val

    M = 0
    indices = []
    for r in clock:
        indices.append(M)
        M += len(r)
    T = 202520252025 % M
    for (i, t) in enumerate(indices):
        if T < t:
            break
    S = T - indices[i - 1]
    return clock[i - 1][S]


if __name__ == '__main__':
    part1()
    part2()
    part3()