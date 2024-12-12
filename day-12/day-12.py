from datetime import date
import numpy as np
import time
import pprint
import math
import re
from copy import deepcopy

from importlib.machinery import SourceFileLoader

lib = SourceFileLoader("lib", "lib.py").load_module()

from aocd import get_data
from aocd import submit

day = 12
path = ""

invalid_token = "."

class Map:

    def __init__(self, fields: list[list[int]], size_x: int, size_y: int):
        self.fields = fields
        self.size_x = size_x
        self.size_y = size_y


def parseInput(input: list[str]) -> Map:

    fields = []

    for x in range(len(input[0])):
        column = []
        for y in range(len(input)):
            column.append(input[y][x])
        fields.append(column)

    size_x = len(input[0])
    size_y = len(input)

    return Map(fields, size_x, size_y)

def is_inside(x: int, y: int, map: Map) -> bool:

    return x >= 0 and x < map.size_x and y >= 0 and y < map.size_y

def get_price(x: int, y: int, map: Map) -> tuple[int, Map]:

    if map.fields[x][y] == invalid_token:
        return (0, map)

    area = [[ 0 for y in range(map.size_y)] for x in range(map.size_x)]
    perimeter = [[ 0 for y in range(map.size_y)] for x in range(map.size_x)]
    new_fields = [[ map.fields[x][y] for y in range(map.size_y)] for x in range(map.size_x)]

    visit(x, y, map, area, perimeter, new_fields, map.fields[x][y])

    total_area = sum([sum(line) for line in area])
    total_perimeter = sum([sum(line) for line in perimeter])

    return (total_area * total_perimeter, Map(new_fields, map.size_x, map.size_y))

def visit(x: int, y: int, map: Map, area: list[list[int]], perimeter: list[list[int]], new_fields: list[list[int]], current_id: str) -> None:

    if not is_inside(x, y, map):
        return

    if new_fields[x][y] == invalid_token:
        return

    if not map.fields[x][y] == current_id:
        return

    perimeter[x][y] = get_perimeter(x, y, map)
    area[x][y] = 1
    new_fields[x][y] = invalid_token

    neighbors = [
        (x-1, y),
        (x+1, y),
        (x, y-1),
        (x, y+1)
    ]

    for neigh_x, neigh_y in neighbors:
        visit(neigh_x, neigh_y, map, area, perimeter, new_fields, current_id)

def get_perimeter(x: int, y: int, map: Map) -> int:

    neighbors = [
        (x-1, y),
        (x+1, y),
        (x, y-1),
        (x, y+1)
    ]

    perimeter = 0

    for neigh_x, neigh_y in neighbors:
        if not is_inside(neigh_x, neigh_y, map):
            perimeter += 1
        elif map.fields[neigh_x][neigh_y] != map.fields[x][y]:
            perimeter += 1

    return perimeter


def part1(data, measure=False):

    startTime = time.time()
    result_1 = 0

    map = parseInput(data)

    for x in range(map.size_x):
        for y in range(map.size_y):
            price, new_map = get_price(x, y, map)
            result_1 += price
            map = new_map

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 1 took: " + str(executionTime) + " s")
    return str(result_1)


def part2(data, measure=False):

    startTime = time.time()
    result_2 = None

    input = parseInput(data)

    # Todo program part 2

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 2 took: " + str(executionTime) + " s")
    return result_2


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

    test_sol_1 = [ "140", "772", "1930" ]
    test_sol_2 = []  # Todo put in test solutions part 2

    test = True

    sol1 = sub1 = False
    sol2 = sub2 = False  # Todo

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

