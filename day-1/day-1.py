from aocd import submit
from aocd import get_data
from datetime import date
import numpy as np
import time
import pprint
import re

from importlib.machinery import SourceFileLoader

lib = SourceFileLoader("lib", "lib.py").load_module()


day = 1
path = ""


def parse_input(input):
    result = None

    pattern = re.compile(r'\d+')

    left_list = []
    right_list = []

    for line in input:
        numbers = pattern.findall(line)
        left_list.append(int(numbers[0]))
        right_list.append(int(numbers[1]))

    result = (left_list, right_list)

    return result


def absolute_value(x):
    return x if x >= 0 else -x


def part1(data, measure=False):
    startTime = time.time()
    result_1 = 0

    (left_list, right_list) = parse_input(data)

    left_list.sort()
    right_list.sort()

    for i in range(len(left_list)):
        result_1 += absolute_value(right_list[i] - left_list[i])

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 1 took: " + str(executionTime) + " s")
    return str(result_1)


def part2(data, measure=False):
    startTime = time.time()
    result_2 = 0

    (left_list, right_list) = parse_input(data)

    right_list_frequencies = dict(
        (number, right_list.count(number)) for number in set(left_list))

    for left_num in left_list:
        result_2 += left_num * right_list_frequencies[left_num]

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 2 took: " + str(executionTime) + " s")
    return str(result_2)


def runTests(test_sol_1, test_sol_2, path):
    test_res_1 = []
    test_res_2 = []

    all_check = True

    paths = lib.get_test_paths(path)

    test_res_1 += list(map(part1, map(lib.get_data_lines, paths)))
    test_res_2 += list(map(part2, map(lib.get_data_lines, paths)))

    success_1 = [(test_sol_1[i] == test_res_1[i])
                 for i in range(len(test_sol_1))]
    success_2 = [
        "Part 2 Test " + str(i + 1) + " " + str(test_sol_2[i] == test_res_2[i])
        for i in range(len(test_sol_2))
    ]

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
    path = "Day " + str(day) + "/"

    test_sol_1 = ["11"]
    test_sol_2 = ["31"]

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
