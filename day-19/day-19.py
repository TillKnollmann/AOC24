from functools import cache, lru_cache
from aocd import submit
from aocd import get_data

import time

from importlib.machinery import SourceFileLoader

lib = SourceFileLoader("lib", "lib.py").load_module()

day = 19
path = ""

test_sol_1 = ["6"]
test_sol_2 = ["16"]

sol_1 = sub_1 = False
sol_2 = sub_2 = False

solvable = set()
manual_cache = dict()


def parse_input(input: list[str]) -> list[str]:

    global solvable

    manual_cache.clear()

    solvable.clear()
    lines = []

    input_total = "\n".join(input)

    solvable_string = input_total.split("\n\n")[0].replace("\n", ", ")
    lines = input_total.split("\n\n")[1].split("\n")

    for word in solvable_string.split(", "):
        if len(word.strip()) > 0:
            solvable.add(word.strip())

    return lines


def num_solutions(current_word: str) -> tuple[bool, int]:

    global solvable, manual_cache

    if len(current_word) == 0:
        return True, 1

    if current_word in manual_cache:
        return manual_cache[current_word]

    total_solutions = 0
    any_solved = False

    for word in solvable:
        if current_word.startswith(word):
            solved, solutions = num_solutions(current_word.removeprefix(word))
            total_solutions += solutions
            if solved:
                any_solved = True

    manual_cache[current_word] = any_solved, total_solutions

    return any_solved, total_solutions


def part_1(data, measure=False):

    startTime = time.time()
    result_1 = 0

    lines = parse_input(data)

    for line in lines:
        solved, _ = num_solutions(line)
        if solved:
            result_1 += 1

    execution_time = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 1 took: " + str(execution_time) + " s")
    return str(result_1)


def part_2(data, measure=False):

    startTime = time.time()
    result_2 = 0

    lines = parse_input(data)

    for line in lines:
        _, solutions = num_solutions(line)
        result_2 += solutions

    execution_time = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 2 took: " + str(execution_time) + " s")
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

    print()

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
    global path, sol_1, sol_2, sub_1, sub_2
    path = "day-" + str(day).zfill(2) + "/"

    test = True

    if test:
        if not run_tests(test_sol_1, test_sol_2, path):
            sub_1 = sub_2 = False

    data_main = get_data(day=day, year=2024).splitlines()

    if sol_1:
        result_1 = part_1(data_main, True)
        print("Result Part 1: " + str(result_1))

    if sol_2:
        result_2 = part_2(data_main, True)
        print("Result Part 2: " + str(result_2))

    print("\n")

    if sub_1:
        submit(int(result_1), part="a", day=day, year=2024)

    if sub_2:
        submit(int(result_2), part="b", day=day, year=2024)


if __name__ == "__main__":
    main()
