from utils import part1_decorator, part2_decorator, part3_decorator


def process_data(data: list[str]):
    return list(map(int, data[0].split(',')))



@part1_decorator
def part1(data: list[str]) -> str:
    vals = process_data(data)
    return sum(set(vals))


@part2_decorator
def part2(data: list[str]) -> str:
    vals = process_data(data)
    return sum(sorted(set(vals))[:20])

    

@part3_decorator
def part3(data: list[str]) -> str:
    vals = process_data(data)
    counter = {}
    for v in vals:
        counter[v] = counter.get(v, 0) + 1
    return max(counter.values())


if __name__ == '__main__':
    part1()
    part2()
    part3()