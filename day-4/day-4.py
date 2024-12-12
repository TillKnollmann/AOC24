import re
from aocd import submit
from aocd import get_data
from datetime import date
import numpy as np
import time
import pprint

from importlib.machinery import SourceFileLoader

lib = SourceFileLoader("lib", "lib.py").load_module()


day = 4
path = ""

xmas_pattern = re.compile(r'XMAS')
samx_pattern = re.compile(r'SAMX')


def parse_input_part_1(input: list[str]):

    # all lines
    result = [line for line in input]

    # all columns
    for column_index in range(len(input[0])):
        column = [line[column_index] for line in input]
        result.append("".join(column))

    # top left to bottom right column 0
    for start_row in range(len(input)):
        top_left_to_bottom_right = []
        column = 0
        for row in range(start_row, len(input)):
            top_left_to_bottom_right.append(input[row][column])
            column += 1
        result.append("".join(top_left_to_bottom_right))

    # top left to bottom right row 0
    for start_column in range(1, len(input[0])):
        top_left_to_bottom_right = []
        row = 0
        for column in range(start_column, len(input[0])):
            top_left_to_bottom_right.append(input[row][column])
            row += 1
        result.append("".join(top_left_to_bottom_right))

    # top right to bottom left column len(input[0])-1
    for start_row in range(len(input)):
        top_right_to_bottom_left = []
        column = len(input[0])-1
        for row in range(start_row, len(input)):
            top_right_to_bottom_left.append(input[row][column])
            column -= 1
        result.append("".join(top_right_to_bottom_left))

     # top right to bottom left row 0
    for start_column in range(1, len(input[0])):
        top_right_to_bottom_left = []
        row = 0
        for column in reversed(range(0, start_column)):
            top_right_to_bottom_left.append(input[row][column])
            row += 1
        result.append("".join(top_right_to_bottom_left))

    return result


def get_xmas_samx_hits(line: str) -> int:

    xmas_hits = len(xmas_pattern.findall(line))
    samx_hits = len(samx_pattern.findall(line))
    return xmas_hits + samx_hits


def parse_input_part_2(input):

    result = []

    for line in input:
        line_splitted = [char for char in line]
        result.append(line_splitted)

    return result


def find_x_mas(puzzle: list[list[str]]) -> int:

    num_of_x_mas: int = 0

    # find all 'a's and check surroundings
    for row in range(1, len(puzzle)-1):
        for column in range(1, len(puzzle[row])-1):
            if puzzle[row][column] == "A":
                if ((puzzle[row-1][column-1] == "M" and puzzle[row+1][column+1] == "S") or (puzzle[row-1][column-1] == "S" and puzzle[row+1][column+1] == "M")) and ((puzzle[row-1][column+1] == "M" and puzzle[row+1][column-1] == "S") or (puzzle[row-1][column+1] == "S" and puzzle[row+1][column-1] == "M")):
                    num_of_x_mas += 1

    return num_of_x_mas


def part1(data, measure=False):
    startTime = time.time()
    result_1 = 0

    input = parse_input_part_1(data)

    for line in input:
        result_1 += get_xmas_samx_hits(line)

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 1 took: " + str(executionTime) + " s")
    return str(result_1)


def part2(data, measure=False):
    startTime = time.time()
    result_2 = 0

    input = parse_input_part_2(data)

    result_2 = find_x_mas(input)

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

    test_sol_1 = ["18"]
    test_sol_2 = ["9"]

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
