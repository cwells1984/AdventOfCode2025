import numpy as np
import re

def get_input(path):
    l = []
    with open(path, 'r') as f:
        for line in f.readlines():
            l.append(re.split("\\s+", line.strip()))
    return np.array(l)


def get_input_part2(path):
    l = []
    with open(path, 'r') as f:
        for line in f.readlines():
            r = []
            for c in line:
                r.append(c)
            l.append(r)
    while len(l[0]) > len(l[-1]):
        l[-1].append(" ")
    a = np.array(l)[:, 0:-1]
    return a


def rows_to_problems(r):
    p = []
    for col in range(len(r[0])):
        p.append(r[:, col].tolist())
    return p


def solve_problem(p):
    operation = p[-1]
    r = -1
    if operation == "+":
        r = 0
        for i in range(0, len(p)-1):
            r += int(p[i])
    if operation == "*":
        r = 1
        for i in range(0, len(p)-1):
            r *= int(p[i])
    return r


def matrix_to_problems(m):
    problems = []
    current_problem = []
    for col in range(len(m[0])-1, -1, -1):
        col_list = m[:, col].tolist()
        if len("".join(col_list).strip()) > 0:
            current_problem.append(int("".join(col_list[0:-1])))
            if col_list[-1] != " ":
                current_problem.append(col_list[-1])
                problems.append(current_problem)
                current_problem = []
    return problems


if __name__ == "__main__":

    # PART 1
    rows = get_input("Day06_Input.txt")
    grand_total = 0
    problems = rows_to_problems(rows)
    for problem in problems:
        grand_total += solve_problem(problem)
    print(f"Grand Total: {grand_total}")

    # PART 2
    problem_matrix = get_input_part2("Day06_Input.txt")
    grand_total = 0
    problems = matrix_to_problems(problem_matrix)
    for problem in problems:
        grand_total += solve_problem(problem)
    print(f"Grand Total: {grand_total}")
