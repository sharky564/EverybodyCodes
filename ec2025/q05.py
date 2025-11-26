from utils import part1_decorator, part2_decorator, part3_decorator


def process_data(data: list[str]):
    return {d.split(':')[0]: list(map(int, d.split(':')[1].split(','))) for d in data}

def make_tree(vals):
    tree = [(vals[0], {})]
    for num in vals[1:]:
        found = False
        for segment in tree:
            if segment[0] > num:
                if segment[1].get('L') is None:
                    segment[1]['L'] = num
                    found = True
                    break
            elif segment[0] < num:
                if segment[1].get('R') is None:
                    segment[1]['R'] = num
                    found = True
                    break
        if not found:
            tree.append((num, {}))
    return tree

@part1_decorator
def part1(data: list[str]) -> str:
    vals = list(process_data(data).values())[0]
    tree = make_tree(vals)
    return int(''.join(map(lambda t: str(t[0]), tree)))
    

@part2_decorator
def part2(data: list[str]) -> str:
    vals = process_data(data)
    trees = {d: make_tree(v) for d, v in vals.items()}
    qualities = list(map(lambda tree: int(''.join(map(lambda t: str(t[0]), tree))), trees.values()))
    return max(qualities) - min(qualities)

@part3_decorator
def part3(data: list[str]) -> str:
    vals = process_data(data)
    trees = [(d, make_tree(v)) for d, v in vals.items()]
    sorted_trees = sorted(
        trees, 
        key=lambda tree: (
            int(''.join(map(lambda t: str(t[0]), tree[1]))),
        ) + tuple([
            int(str(segment[1].get('L', '')) + str(segment[0]) + str(segment[1].get('R', '')))
            for segment in tree[1]
        ]) + (int(tree[0]),),
        reverse=True
    )
    return sum(map(lambda i: i[0] * int(i[1][0]), enumerate(sorted_trees, 1)))
    


if __name__ == '__main__':
    part1()
    part2()
    part3()