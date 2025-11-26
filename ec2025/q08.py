from utils import part1_decorator, part2_decorator, part3_decorator


def process_data(data: list[str]):
    return list(map(int, data[0].split(',')))


@part1_decorator
def part1(data: list[str]) -> str:
    vals = process_data(data)
    N = 32
    return sum(1 for i, j in zip(vals, vals[1:]) if abs(i - j) == N // 2)
    
    
@part2_decorator
def part2(data: list[str]) -> str:
    vals = process_data(data)
    chords = {}
    knots = 0
    for i, j in zip(vals, vals[1:]):
        w, x = sorted([i, j])
        for c in filter(lambda t: t not in [w, x], chords):
            for d in filter(lambda t: t not in [w, x], chords[c]):
                if w < c < x < d or c < w < d < x:
                    knots += 1
        chords[w] = chords.get(w, []) + [x]
    return knots


@part3_decorator
def part3(data: list[str]) -> str:
    vals = process_data(data)
    N = 256
    chords = {}
    for i, j in zip(vals, vals[1:]):
        w, x = sorted([i, j])
        chords[w] = chords.get(w, []) + [x]
    
    max_found = 0
    max_pair = None
    for i in range(1, N + 1):
        for j in range(i + 1, N + 1):
            count = 0
            for c in filter(lambda t: t not in [i, j], chords):
                for d in filter(lambda t: t not in [i, j], chords[c]):
                    if i < c < j < d or c < i < d < j:
                        count += 1
            if i in chords and j in chords[i]:
                count += 1
            if count > max_found:
                max_found = count
                max_pair = (i, j)
    return max_found, max_pair


if __name__ == '__main__':
    part1()
    part2()
    part3()