from pathlib import Path


def part1_decorator(func):
    input_dir = Path.cwd() / 'ec2025/input_pt1.txt'

    def wrapper(*args, **kwargs):
        with open(input_dir, 'r') as f:
            out = f.readlines()
            print('Part 1:', func(out, *args, **kwargs))
    return wrapper

def part2_decorator(func):
    input_dir = Path.cwd() / 'ec2025/input_pt2.txt'

    def wrapper(*args, **kwargs):
        with open(input_dir, 'r') as f:
            out = f.readlines()
            print('Part 2:', func(out, *args, **kwargs))
    return wrapper

def part3_decorator(func):
    input_dir = Path.cwd() / 'ec2025/input_pt3.txt'

    def wrapper(*args, **kwargs):
        with open(input_dir, 'r') as f:
            out = f.readlines()
            print('Part 3:', func(out, *args, **kwargs))
    return wrapper