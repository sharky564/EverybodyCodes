from utils import part1_decorator, part2_decorator, part3_decorator
from functools import cache


def process_data(data: list[str]):
    return [list(line.strip()) for line in data]

@part1_decorator
def part1(data: list[str]) -> str:
    vals = process_data(data)
    N = len(vals)
    M = len(vals[0])
    T = 4

    dragon = None
    sheep = []
    for i in range(N):
        for j in range(M):
            if vals[i][j] == 'D':
                dragon = (i, j)
            elif vals[i][j] == 'S':
                sheep.append((i, j))

    known = {}
    def reachable(curr_sq, n):
        if (curr_sq, n) not in known:
            if n == 0:
                known[(curr_sq, n)] = {curr_sq}
            else:
                adj_sq = filter(lambda sq: 0 <= sq[0] < N and 0 <= sq[1] < M,
                    ((curr_sq[0] + i, curr_sq[1] + j) 
                    for i, j in [(0, 0), (1, 2), (2, 1), (-1, 2), (2, -1), (1, -2), (-2, 1), (-1, -2), (-2, -1)])
                )
                out = set()
                for sq in adj_sq:
                    out = out.union(reachable(sq, n - 1))
                known[(curr_sq, n)] = out
        return known[(curr_sq, n)]
    
    return sum(sq in sheep for sq in reachable(dragon, T))




@part2_decorator
def part2(data: list[str]) -> str:
    vals = process_data(data)
    N = len(vals)
    M = len(vals[0])
    T = 20

    dragon = None
    sheep = []
    safe = []
    for i in range(N):
        for j in range(M):
            if vals[i][j] == 'D':
                dragon = (i, j)
            elif vals[i][j] == 'S':
                sheep.append((i, j))
            elif vals[i][j] == '#':
                safe.append((i, j))

    known = {}
    def reachable(curr_sq, n):
        if (curr_sq, n) not in known:
            if n == 0:
                known[(curr_sq, n)] = {curr_sq}
            else:
                adj_sq = filter(lambda sq: 0 <= sq[0] < N and 0 <= sq[1] < M,
                    ((curr_sq[0] + i, curr_sq[1] + j) 
                    for i, j in [(1, 2), (2, 1), (-1, 2), (2, -1), (1, -2), (-2, 1), (-1, -2), (-2, -1)])
                )
                out = set()
                for sq in adj_sq:
                    out = out.union(reachable(sq, n - 1))
                known[(curr_sq, n)] = out
        return known[(curr_sq, n)]
    
    total = 0
    for t in range(1, T + 1):
        for sq in reachable(dragon, t):
            if sq in sheep and sq not in safe:
                total += 1
                sheep.remove(sq)
        sheep = list(filter(
            lambda sq: 0 <= sq[0] < N and 0 <= sq[1] < M, 
            map(lambda sq: (sq[0] + 1, sq[1]), sheep)
        ))
        for sq in reachable(dragon, t):
            if sq in sheep and sq not in safe:
                total += 1
                sheep.remove(sq)

    return total


@part3_decorator
def part3(data: list[str]) -> str:
    vals = process_data(data)
    N = len(vals)
    M = len(vals[0])

    dragon = None
    sheep = []
    safe = []
    for i in range(N):
        for j in range(M):
            if vals[i][j] == 'D':
                dragon = (i, j)
            elif vals[i][j] == 'S':
                sheep.append((i, j))
            elif vals[i][j] == '#':
                safe.append((i, j))

    @cache
    def calculate(curr_sq, sheep_set, turn):
        if len(sheep_set) == 0:
            return 1
        answer = 0
        if turn:
            for direction in [(1, 2), (2, 1), (-1, 2), (2, -1), (1, -2), (-2, 1), (-1, -2), (-2, -1)]:
                new_sq = (curr_sq[0] + direction[0], curr_sq[1] + direction[1])
                if 0 <= new_sq[0] < N and 0 <= new_sq[1] < M:
                    new_sheep_set = sheep_set
                    if new_sq not in safe:
                        new_sheep_set = frozenset(set(sheep_set) - {new_sq})
                    answer += calculate(new_sq, new_sheep_set, not turn)
        else:
            can_move = False
            for curr_sheep_sq in sheep_set:
                next_sheep_sq = (curr_sheep_sq[0] + 1, curr_sheep_sq[1])
                if curr_sheep_sq[0] == N - 1 or next_sheep_sq != curr_sq or next_sheep_sq in safe:
                    can_move = True
                if 0 <= curr_sheep_sq[0] < N - 1 and (next_sheep_sq in safe or next_sheep_sq != curr_sq):
                    new_sheep_set = set(sheep_set)
                    new_sheep_set.remove(curr_sheep_sq)
                    new_sheep_set.add(next_sheep_sq)

                    answer += calculate(curr_sq, frozenset(new_sheep_set), not turn)
            if not can_move:
                answer = calculate(curr_sq, sheep_set, not turn)
        
        return answer
    
    return calculate(dragon, frozenset(sheep), False)



if __name__ == '__main__':
    part1()
    part2()
    part3()