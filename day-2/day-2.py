from datetime import date
import numpy as np
import time
import pprint

from importlib.machinery import SourceFileLoader

lib = SourceFileLoader("lib", "lib.py").load_module()

from aocd import get_data
from aocd import submit

import re

day = 2
path = ""


def parseInput(input):
    result = []

    pattern = re.compile(r'\d+')

    for line in input:
        result.append(list(int(num) for num in pattern.findall(line)))

    return result

def is_level_safe_part_1(level: list[int]) -> bool:
    (violations, violations_reversed) = get_all_violations(level)
    return len(violations) == 0 or len(violations_reversed) == 0

def is_level_safe_part_2(level: list[int]) -> bool:

    (violations, violations_reversed) = get_all_violations(level)
    if len(violations) > 2 and len(violations_reversed) > 2:
        return False
    elif len(violations) == 0 or len(violations_reversed) == 0:
        return True
    else:
        if len(violations) <= 2:
            if can_level_be_fixed(level, violations):
                return True
        if len(violations_reversed) <= 2:
            reversed = [num for num in level]
            reversed.reverse()
            if can_level_be_fixed(reversed, violations_reversed):
                return True
        return False

def can_level_be_fixed(level: list[int], violations: list[int]):
    if len(violations) > 2:
        return False
    if len(violations) == 0:
        return True
    adapted = cutout(level, violations[0])
    if (is_level_safe_part_1(adapted)):
        return True
    elif (violations[0] + 1 < len(level)):
        adapted = cutout(level, violations[0]+1)
        if is_level_safe_part_1(adapted):
            return True
    elif (violations[0] + 2 < len(level)):
        adapted = cutout(level, violations[0]+2)
        if is_level_safe_part_1(adapted):
            return True
    else:
        return False

def cutout(level: list[int], index:int) -> list[int]:
    if index == 0:
        return level[1:]
    elif index == len(level)-1:
        return level[:len(level)-1]
    else:
        return level[:index] + level[index+1:]

def get_all_violations(level: list[int]) -> list[int]:

    violations = get_violations(level)
    reversed = [num for num in level]
    reversed.reverse()
    violations_reversed = get_violations(reversed)

    return (violations, violations_reversed)

def get_violations(level: list[int]) -> list[int]:

    # Assumption: level is ascending
    violations = []
    for i in range(0, len(level)-1):
        if not is_pair_safe(level[i], level[i+1]):
            violations.append(i)

    return violations

def is_pair_safe(first: int, second: int) -> bool:
    if first >= second or second - first > 3:
        return False
    return True


def part1(data, measure=False):
    startTime = time.time()
    result_1 = 0

    input = parseInput(data)

    for level in input:
        if is_level_safe_part_1(level):
            result_1 += 1


    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 1 took: " + str(executionTime) + " s")
    return str(result_1)


def part2(data, measure=False):
    startTime = time.time()
    result_2 = 0

    input = parseInput(data)

    for level in input:
        if is_level_safe_part_2(level):
            result_2 += 1

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 2 took: " + str(executionTime) + " s")
    return str(result_2)


def runTests(test_sol_1, test_sol_2, path):
    test_res_1 = []
    test_res_2 = []

    all_check = True

    paths = lib.getTestPaths(path)

    test_res_1 += list(map(part1, map(lib.getDataLines, paths)))
    test_res_2 += list(map(part2, map(lib.getDataLines, paths)))

    success_1 = [(test_sol_1[i] == test_res_1[i]) for i in range(len(test_sol_1))]
    success_2 = [(test_sol_2[i] == test_res_2[i]) for i in range(len(test_sol_2))]

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
    global path
    path = "day-" + str(day) + "/"

    test_sol_1 = [ "2" ]
    test_sol_2 = [ "4" ]

    test = True

    sol1 = sub1 = False
    sol2 = sub2 = True  # Todo

    if test:
        if not runTests(test_sol_1, test_sol_2, path):
            sub1 = sub2 = False

    data_main = get_data(day=day, year=2024).splitlines()

    if sol1:
        result_1 = part1(data_main, True)
        print("Result Part 1: " + str(result_1))

    if sol2:
        result_2 = part2(data_main, True)
        print("Result Part 2: " + str(result_2))

    print("\n")

    if sub1:
        submit(int(result_1), part="a", day=day, year=2024)

    if sub2:
        submit(int(result_2), part="b", day=day, year=2024)


if __name__ == "__main__":
    main()

