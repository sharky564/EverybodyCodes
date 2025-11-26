from utils import part1_decorator, part2_decorator, part3_decorator


def process_data(data: list[str]):
    strings = [x.split(':') for x in data]
    return {int(k): v.strip() for k, v in strings}

def similarity(str1, str2):
    return sum(i == j for i, j in zip(str1, str2))


def match(p1, p2, c):
    return all(z in [x, y] for x, y, z in zip(p1, p2, c))


@part1_decorator
def part1(data: list[str]) -> str:
    vals = process_data(data)
    sim1 = similarity(vals[1], vals[3])
    sim2 = similarity(vals[2], vals[3])
    return sim1 * sim2
    


@part2_decorator
def part2(data: list[str]) -> str:
    vals = process_data(data)
    total = 0
    for child in vals:
        sorted_parents = sorted(filter(lambda t: t != child, vals), key=lambda parent: similarity(vals[parent], vals[child]), reverse=True)
        for i in range(len(sorted_parents)):
            for j in range(i + 1, len(sorted_parents)):
                parent1, parent2 = sorted_parents[i], sorted_parents[j]
                if match(vals[parent1], vals[parent2], vals[child]):
                    total += similarity(vals[parent1], vals[child]) * similarity(vals[parent2], vals[child])
                    break
            else:
                continue
            break
    return total


@part3_decorator
def part3(data: list[str]) -> str:
    vals = process_data(data)
    all_parents = {}
    for child in vals:
        sorted_parents = sorted(filter(lambda t: t != child, vals), key=lambda parent: similarity(vals[parent], vals[child]), reverse=True)
        for i in range(len(sorted_parents)):
            for j in range(i + 1, len(sorted_parents)):
                parent1, parent2 = sorted_parents[i], sorted_parents[j]
                if match(vals[parent1], vals[parent2], vals[child]):
                    all_parents[child] = [parent1, parent2]
                    break
            else:
                continue
            break
    families = []
    for child, parents in all_parents.items():
        members = set(parents + [child])
        relevant_families = list(filter(lambda family: any(f in family for f in members), families))
        combined = members
        for family in relevant_families:
            families.remove(family)
            combined = combined.union(family)
        families.append(combined)
    
    return sum(max(families, key=len))



if __name__ == '__main__':
    part1()
    part2()
    part3()