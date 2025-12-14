import copy
import math
import re
import time
from importlib.machinery import SourceFileLoader

import numpy as np
from aocd import get_data
from aocd import submit

lib = SourceFileLoader("lib", "lib.py").load_module()


day = 5
path = ""


def parse_input(input) -> tuple[set[tuple[int, int]], list[list[int]]]:

    complete_input = "\n".join(input)
    rules_input = complete_input.split("\n\n")[0]
    orderings_input = complete_input.split("\n\n")[1]

    number_pattern = re.compile(r'\d+')

    smaller_to_greater = set()
    for rule in rules_input.split("\n"):
        numbers = number_pattern.findall(rule)
        smaller_to_greater.add((int(numbers[0]), int(numbers[1])))

    orderings = [[int(num) for num in number_pattern.findall(ordering_line)]
                 for ordering_line in orderings_input.split("\n")]

    return smaller_to_greater, orderings


def is_valid(ordering: list[int], rules: set[tuple[int, int]]) -> bool:
    for i in range(len(ordering)-1):
        for j in range(i+1, len(ordering)):
            if (ordering[j], ordering[i]) in rules:
                return False
    return True


def fix(ordering: list[int], rules: set[tuple[int, int]]) -> list[int]:

    new_ordering = copy.deepcopy(ordering)

    fix_applied = True
    while fix_applied:
        fix_applied = False
        for i in range(len(new_ordering)-1):
            for j in range(i+1, len(new_ordering)):
                if (new_ordering[j], new_ordering[i]) in rules:
                    temp = new_ordering[i]
                    new_ordering[i] = new_ordering[j]
                    new_ordering[j] = temp
                    fix_applied = True

    return new_ordering


def get_middle(ordering: list[int]):
    if len(ordering) % 2 == 0:
        return ordering[len(ordering)/2]
    else:
        return ordering[math.floor(len(ordering)/2)]


def part_1(data, measure=False):
    startTime = time.time()
    result_1 = 0

    smaller_greater, orderings = parse_input(data)

    for ordering in orderings:
        if is_valid(ordering, smaller_greater):
            result_1 += get_middle(ordering)

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 1 took: " + str(executionTime) + " s")
    return str(result_1)


def part_2(data, measure=False):
    startTime = time.time()
    result_2 = 0

    smaller_greater, orderings = parse_input(data)

    for ordering in orderings:
        if not is_valid(ordering, smaller_greater):
            new_ordering = fix(ordering, smaller_greater)
            result_2 += get_middle(new_ordering)

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 2 took: " + str(executionTime) + " s")
    return str(result_2)


def run_tests(test_sol_1, test_sol_2, path):
    test_res_1 = []
    test_res_2 = []

    all_check = True

    paths = lib.get_test_paths(path)

    test_res_1 += list(map(part_1, map(lib.get_data_lines, paths)))
    test_res_2 += list(map(part_2, map(lib.get_data_lines, paths)))

    success_1 = [(test_sol_1[i] == test_res_1[i])
                 for i in range(len(test_sol_1))]
    success_2 = [(test_sol_2[i] == test_res_2[i])
                 for i in range(len(test_sol_2))]

    for i in range(len(test_sol_1)):
        if success_1[i]:
            print("Part 1 Test " + str(i + 1) + " Succeeded!")
        else:
            print(
                "Part 1 Test "
                + str(i + 1)
                + " Failed! Expected "
                + str(test_sol_1[i])
                + " received "
                + test_res_1[i]
            )
            all_check = False

    for i in range(len(test_sol_2)):
        if success_2[i]:
            print("Part 2 Test " + str(i + 1) + " Succeeded!")
        else:
            print(
                "Part 2 Test "
                + str(i + 1)
                + " Failed! Expected "
                + str(test_sol_2[i])
                + " received "
                + test_res_2[i]
            )
            all_check = False

    return all_check


def main():
    global path, sol_1, sol_2, sub_1, sub_2, result_2, result_1
    path = "day-" + str(day).zfill(2) + "/"

    test_sol_1 = ["143"]
    test_sol_2 = ["123"]

    test = True

    sol1 = sub_1 = False
    sol2 = sub_2 = False

    if test:
        if not run_tests(test_sol_1, test_sol_2, path):
            sub_1 = sub_2 = False

    data_main = get_data(day=day, year=2024).splitlines()

    if sol1:
        result_1 = part_1(data_main, True)
        print("Result Part 1: " + str(result_1))

    if sol2:
        result_2 = part_2(data_main, True)
        print("Result Part 2: " + str(result_2))

    print("\n")

    if sub_1:
        submit(int(result_1), part="a", day=day, year=2024)

    if sub_2:
        submit(int(result_2), part="b", day=day, year=2024)


if __name__ == "__main__":
    main()
