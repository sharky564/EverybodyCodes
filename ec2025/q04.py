from utils import part1_decorator, part2_decorator, part3_decorator
from math import ceil


def process_data(data: list[str]):
    return list(map(int, data))

def process_data_3(data: list[str]):
    return list(map(lambda s: (int(s), int(s)) if '|' not in s else tuple(map(int, s.split('|'))), data))

@part1_decorator
def part1(data: list[str]) -> str:
    teeth = process_data(data)
    turns = [2025]
    for i, (curr_gear, next_gear) in enumerate(zip(teeth, teeth[1:])):
        curr_num_turns = turns[i]
        turns.append(curr_gear * curr_num_turns / next_gear)
    return int(turns[-1])

@part2_decorator
def part2(data: list[str]) -> str:
    teeth = process_data(data)
    ratio = 1
    for curr_gear, next_gear in zip(teeth, teeth[1:]):
        ratio *= curr_gear / next_gear
    return ceil(10000000000000 / ratio)

    

@part3_decorator
def part3(data: list[str]) -> str:
    teeth = process_data_3(data)
    turns = [100]
    for i, (curr_gear, next_gear) in enumerate(zip(teeth, teeth[1:])):
        curr_num_turns = turns[i]
        turns.append(curr_gear[1] * curr_num_turns / next_gear[0])
    return int(turns[-1])


if __name__ == '__main__':
    part1()
    part2()
    part3()
