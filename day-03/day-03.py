import re
import time
from importlib.machinery import SourceFileLoader

import numpy as np
from aocd import get_data
from aocd import submit

lib = SourceFileLoader("lib", "lib.py").load_module()


day = 3
path = ""


def parse_input(input):
    result = None

    result = "".join(input)

    return result


def get_enabled_multiplications(memory: str) -> list[str]:

    enabled = True

    segment_memory = re.split(r'(do\(\)|don\'t\(\))', memory)

    enabled_multiplications = []
    for segment in segment_memory:
        if segment.startswith("don't()"):
            enabled = False
        elif segment.startswith("do()"):
            enabled = True
        if enabled:
            multiplications = get_multiplications(segment)
            for mult in multiplications:
                enabled_multiplications.append(mult)

    return enabled_multiplications


def get_multiplications(memory: str) -> list[str]:

    pattern = re.compile(r'mul\([0-9]{1,3},[0-9]{1,3}\)')

    return pattern.findall(memory)


def interpret_multiplication(mult: str) -> int:

    pattern = re.compile(r'\d+')

    numbers = [int(num) for num in pattern.findall(mult)]
    return numbers[0] * numbers[1]


def part_1(data, measure=False):
    startTime = time.time()
    result_1 = 0

    input = parse_input(data)

    multiplications = get_multiplications(input)
    for multiplication in multiplications:
        result_1 += interpret_multiplication(multiplication)

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 1 took: " + str(executionTime) + " s")
    return str(result_1)


def part_2(data, measure=False):
    startTime = time.time()
    result_2 = 0

    input = parse_input(data)

    multiplications = get_enabled_multiplications(input)
    for multiplication in multiplications:
        result_2 += interpret_multiplication(multiplication)

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

    test_sol_1 = ["161", "161"]
    test_sol_2 = ["161", "48"]

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
