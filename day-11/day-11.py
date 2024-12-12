from aocd import submit
from aocd import get_data
from datetime import date
import numpy as np
import time
import pprint
import math
import re
from copy import deepcopy

from importlib.machinery import SourceFileLoader

lib = SourceFileLoader("lib", "lib.py").load_module()


day = 11
path = ""


def parseInput(input: list[str]) -> dict[int, int]:

    num_pattern = re.compile(r'\d+')

    result = dict()

    for num_string in num_pattern.findall(input[0]):
        num = int(num_string)
        if not num in result:
            result[num] = 0
        result[num] = 1

    return result


def apply_rules_to_stone(stone: int) -> list[int]:

    if stone == 0:
        return [1]
    elif len(str(stone)) % 2 == 0:
        stone_str = str(stone)
        stone_1 = int(stone_str[:int(len(stone_str)/2)])
        stone_2 = int(stone_str[int(len(stone_str)/2):])
        return [stone_1, stone_2]
    else:
        return [stone*2024]


def blink(stones: dict[int, int]) -> dict[int, int]:

    new_stones = dict()

    for stone, frequency in stones.items():
        successors = apply_rules_to_stone(stone)
        for successor in successors:
            if not successor in new_stones:
                new_stones[successor] = 0
            new_stones[successor] += frequency

    return new_stones


def part1(data, measure=False):

    startTime = time.time()
    result_1 = None

    stones = parseInput(data)

    for i in range(25):
        stones = blink(stones)

    result_1 = sum(stones.values())

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 1 took: " + str(executionTime) + " s")
    return str(result_1)


def part2(data, measure=False):

    startTime = time.time()
    result_2 = None

    stones = parseInput(data)

    for i in range(75):
        stones = blink(stones)

    result_2 = sum(stones.values())

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
    global path
    path = "day-" + str(day) + "/"

    test_sol_1 = ["55312"]
    test_sol_2 = ["65601038650482"]

    test = True

    sol1 = sub1 = False
    sol2 = sub2 = False

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
