from utils import part1_decorator, part2_decorator, part3_decorator


def process_data(data: list[str]):
    names = list(map(lambda c: c.strip(), data[0].split(',')))
    sequences = {}
    for line in data[2:]:
        c, chars = line.split(' > ')
        chars = list(map(lambda c: c.strip(), chars.split(',')))
        sequences[c] = chars
    return names, sequences

def satisfying(name, sequences):
    return all(
        next_char in sequences[curr_char] 
        for (curr_char, next_char) in zip(name, name[1:]) 
        if curr_char in sequences
    )

@part1_decorator
def part1(data: list[str]) -> str:
    names, sequences = process_data(data)
    for name in names:
        if satisfying(name, sequences):
            return name
    
    
@part2_decorator
def part2(data: list[str]) -> str:
    names, sequences = process_data(data)
    total = 0
    for i, name in enumerate(names, 1):
        if satisfying(name, sequences):
            total += i
    return total


@part3_decorator
def part3(data: list[str]) -> str:
    names, sequences = process_data(data)
    known = {}
    def dfs(curr_name):
        if curr_name not in known:
            total = 0
            if 7 <= len(curr_name) <= 11:
                total += 1
            if len(curr_name) >= 11:
                known[curr_name] = total
            else:
                c = curr_name[-1]
                if c not in sequences:
                    known[curr_name] = total
                else:
                    known[curr_name] = total + sum(dfs(curr_name + d) for d in sequences[c])
            return known[curr_name]
        return 0

    return sum(map(dfs, filter(lambda name: satisfying(name, sequences), names)))


if __name__ == '__main__':
    part1()
    part2()
    part3()