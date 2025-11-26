from utils import part1_decorator, part2_decorator, part3_decorator

def process_data(data: list[str]):
    return [int(line) for line in data]

def move1(arr):
    output = list(arr)
    for i in range(len(output) - 1):
        if output[i] > output[i + 1]:
            output[i] -= 1
            output[i + 1] += 1
    return output

def move2(arr):
    output = list(arr)
    for i in range(len(output) - 1):
        if output[i] < output[i + 1]:
            output[i] += 1
            output[i + 1] -= 1
    return output

def flatten(arr):
    rounds = 0
    phase_change = False
    new_arr = None
    while True:
        if not phase_change:
            new_arr = move1(arr)
            if new_arr == arr:
                phase_change = True
            else:
                arr = new_arr
                rounds += 1
        else:
            mean = sum(arr) // len(arr)
            rounds += sum(abs(x - mean) for x in arr) // 2
            break
    return rounds

@part1_decorator
def part1(data: list[str]) -> str:
    vals = process_data(data)
    def checksum(arr):
        return sum(map(lambda x, y: x * y, arr, range(1, len(arr) + 1)))
    rounds = 0
    phase_change = False
    while rounds < 10:
        if not phase_change:
            new_vals = move1(vals)
            if new_vals == vals:
                phase_change = True
            else:
                vals = new_vals
                rounds += 1
        else:
            new_vals = move2(vals)
            if new_vals == vals:
                break
            else:
                vals = new_vals
                rounds += 1
    return checksum(vals)


@part2_decorator
def part2(data: list[str]) -> str:
    vals = process_data(data)
    return flatten(vals)


@part3_decorator
def part3(data: list[str]) -> str:
    vals = process_data(data)
    return flatten(vals)

# 1 4 18 14 19 10
# 1 4 10 10 10 10
# 0 0 8 4 9 0
# 0 0 6 6 7 2       2
# 0 0 6 6 6 3       1
# 0 0 5 5 5 6       3
# 1 4 15 15 15 16
# 11 11 11 11 11 11 17


if __name__ == '__main__':
    part1()
    part2()
    part3()