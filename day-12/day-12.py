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


day = 12
path = ""

invalid_token = "."


class Area(list[list[int]]):
    pass


def parseInput(input: list[str]) -> Area:

    area = []

    for x in range(len(input[0])):
        column = []
        for y in range(len(input)):
            column.append(input[y][x])
        area.append(column)

    return area


def is_inside(x: int, y: int, area: Area) -> bool:

    return x >= 0 and x < len(area[0]) and y >= 0 and y < len(area[0])


def get_price(x: int, y: int, area: Area, part_two: bool) -> tuple[int, Area]:

    if area[x][y] == invalid_token:
        return (0, area)

    area_of_token = [[0 for y in range(len(area[x]))]
                     for x in range(len(area))]
    perimeter = [[0 for y in range(len(area[x]))] for x in range(len(area))]
    new_area = [[area[x][y]
                 for y in range(len(area[x]))] for x in range(len(area))]

    visit(x, y, area, area_of_token, perimeter, new_area, area[x][y])

    total_area_of_token = sum([sum(line) for line in area_of_token])
    total_perimeter = sum([sum(line) for line in perimeter])

    if part_two:
        total_perimeter = get_number_of_sides(area_of_token)

    return (total_area_of_token * total_perimeter, new_area)


def visit(x: int, y: int, area: Area, area_of_token: Area, perimeter: Area, new_area: Area, token: str) -> None:

    if not is_inside(x, y, area):
        return

    if new_area[x][y] == invalid_token:
        return

    if not area[x][y] == token:
        return

    perimeter[x][y] = get_perimeter(x, y, area)
    area_of_token[x][y] = 1
    new_area[x][y] = invalid_token

    neighbors = [
        (x-1, y),
        (x+1, y),
        (x, y-1),
        (x, y+1)
    ]

    for neigh_x, neigh_y in neighbors:
        visit(neigh_x, neigh_y, area, area_of_token, perimeter, new_area, token)


def get_perimeter(x: int, y: int, area: Area) -> int:

    neighbors = [
        (x-1, y),
        (x+1, y),
        (x, y-1),
        (x, y+1)
    ]

    perimeter = 0

    for neigh_x, neigh_y in neighbors:
        if not is_inside(neigh_x, neigh_y, area):
            perimeter += 1
        elif area[neigh_x][neigh_y] != area[x][y]:
            perimeter += 1

    return perimeter


def get_number_of_sides(area: Area) -> int:

    adapted_area = [[area[x][y]
                     for y in range(len(area[x]))] for x in range(len(area))]
    adapted_area = trim(adapted_area)
    adapted_area = add_border(adapted_area)

    corner_patterns = [
        ([(0, 0), (1, 0), (0, 1)], [(1, 1)]),
        ([(0, 0), (1, 0), (1, 1)], [(0, 1)]),
        ([(0, 0), (0, 1), (1, 1)], [(1, 0)]),
        ([(1, 0), (0, 1), (1, 1)], [(0, 0)]),
        ([(1, 1)], [(0, 0), (1, 0), (0, 1)]),
        ([(0, 1)], [(0, 0), (1, 0), (1, 1)]),
        ([(1, 0)], [(0, 0), (0, 1), (1, 1)]),
        ([(0, 0)], [(1, 0), (0, 1), (1, 1)])
    ]
    double_patterns = [
        ([(0, 0), (1, 1)], [(1, 0), (0, 1)]),
        ([(1, 0), (0, 1)], [(0, 0), (1, 1)])
    ]

    corners = 0

    for x in range(len(adapted_area) - 1):
        for y in range(len(adapted_area[x]) - 1):
            for pattern_out, pattern_in in corner_patterns:
                if all(adapted_area[x + dx][y + dy] == 0 for dx, dy in pattern_out) and all(adapted_area[x + dx][y + dy] == 1 for dx, dy in pattern_in):
                    corners += 1
            for pattern_out, pattern_in in double_patterns:
                if all(adapted_area[x + dx][y + dy] == 0 for dx, dy in pattern_out) and all(adapted_area[x + dx][y + dy] == 1 for dx, dy in pattern_in):
                    corners += 2

    return corners


def trim(area: Area) -> Area:

    size_x = len(area)
    size_y = len(area[0])

    min_x = size_x
    max_x = 0
    min_y = size_y
    max_y = 0

    for x in range(size_x):
        for y in range(size_y):
            if area[x][y] == 1:
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)

    return [x[min_y:max_y+1] for x in area[min_x:max_x + 1]]


def add_border(area: Area) -> Area:

    new_area = [[0 for _ in range(len(area[0]) + 2)]
                for _ in range(len(area) + 2)]

    for x in range(len(area)):
        for y in range(len(area[x])):
            new_area[x+1][y+1] = area[x][y]

    return new_area


def part1(data, measure=False):

    startTime = time.time()
    result_1 = 0

    area = parseInput(data)

    for x in range(len(area)):
        for y in range(len(area[x])):
            price, new_area = get_price(x, y, area, False)
            result_1 += price
            area = new_area

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 1 took: " + str(executionTime) + " s")
    return str(result_1)


def part2(data, measure=False):

    startTime = time.time()
    result_2 = 0

    area = parseInput(data)

    for x in range(len(area)):
        for y in range(len(area[x])):
            price, new_area = get_price(x, y, area, True)
            result_2 += price
            area = new_area

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

    test_sol_1 = ["140", "772", "1930", "692", "1184"]
    test_sol_2 = ["80", "436", "1206", "236", "368"]

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
