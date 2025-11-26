from utils import part1_decorator, part2_decorator, part3_decorator

def clamp(x, a, b):
    assert a <= b, 'Cannot clamp if a > b'
    return max(a, min(b, x))

def process_data(data: list[str]):
    names, _, directions = data
    names = list(map(lambda t: t.strip(), names.split(',')))
    directions = list(map(lambda t: t.strip(), directions.split(',')))
    translated_dirs = map(lambda s: int(s[1:]) if s[0] == 'R' else -int(s[1:]), directions)
    return names, translated_dirs

@part1_decorator
def part1(data: list[str]) -> str:
    names, translated_dirs = process_data(data)
    curr_ind = 0
    max_ind = len(names) - 1
    for num in translated_dirs:
        curr_ind = clamp(curr_ind + num, 0, max_ind)
    return names[curr_ind]

@part2_decorator
def part2(data: list[str]) -> str:
    names, translated_dirs = process_data(data)
    curr_ind = 0
    size = len(names)
    for num in translated_dirs:
        curr_ind = (curr_ind + num) % size
    return names[curr_ind]

@part3_decorator
def part3(data: list[str]) -> str:
    names, translated_dirs = process_data(data)
    size = len(names)
    for num in translated_dirs:
        names[num % size], names[0] = names[0], names[num % size]
    return names[0]


if __name__ == '__main__':
    part1()
    part2()
    part3()