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


day = 10
path = ""


class Game:

    def __init__(self, map: list[list[int]], size_x: int, size_y: int):
        self.map = map
        self.size_x = size_x
        self.size_y = size_y


def parse_input(input: list[str]) -> Game:

    map = []

    size_x = len(input[0])
    size_y = len(input)

    for x in range(len(input[0])):
        map.append([int(input[y][x]) for y in range(len(input))])

    return Game(map, size_x, size_y)


def get_reachable_summits(game: Game, x: int, y: int, reachable_summits: list[list[set[tuple[int, int]]]]) -> set[tuple[int, int]]:

    if game.map[x][y] == 9:
        return {(x, y)}

    neighbors = [
        (x-1, y),
        (x+1, y),
        (x, y-1),
        (x, y+1)
    ]

    union = set()

    for (neighbor_x, neightbor_y) in neighbors:
        if is_inside(game, neighbor_x, neightbor_y):
            if game.map[x][y] == game.map[neighbor_x][neightbor_y] - 1:
                for summit in reachable_summits[neighbor_x][neightbor_y]:
                    union.add(summit)

    return union


def get_number_of_trails(game: Game, x: int, y: int, reachable_trails: list[list[set[tuple[int, int]]]]) -> set[tuple[int, int]]:

    if game.map[x][y] == 9:
        return 1

    neighbors = [
        (x-1, y),
        (x+1, y),
        (x, y-1),
        (x, y+1)
    ]

    sum = 0

    for (neighbor_x, neightbor_y) in neighbors:
        if is_inside(game, neighbor_x, neightbor_y):
            if game.map[x][y] == game.map[neighbor_x][neightbor_y] - 1:
                sum += reachable_trails[neighbor_x][neightbor_y]

    return sum


def is_inside(game: Game, x: int, y: int) -> bool:

    return x >= 0 and x < game.size_x and y >= 0 and y < game.size_y


def part_1(data, measure=False):

    startTime = time.time()
    result_1 = 0

    game = parse_input(data)

    reachable_summits = [[None for y in range(
        game.size_y)] for x in range(game.size_x)]

    for height in reversed(range(10)):
        for x in range(game.size_x):
            for y in range(game.size_y):
                if game.map[x][y] == height:
                    reachable_summits[x][y] = get_reachable_summits(
                        game, x, y, reachable_summits)

    for x in range(game.size_x):
        for y in range(game.size_y):
            if game.map[x][y] == 0:
                result_1 += len(reachable_summits[x][y])

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 1 took: " + str(executionTime) + " s")
    return str(result_1)


def part_2(data, measure=False):

    startTime = time.time()
    result_2 = 0

    game = parse_input(data)

    reachable_trails = [[None for y in range(
        game.size_y)] for x in range(game.size_x)]

    for height in reversed(range(10)):
        for x in range(game.size_x):
            for y in range(game.size_y):
                if game.map[x][y] == height:
                    reachable_trails[x][y] = get_number_of_trails(
                        game, x, y, reachable_trails)

    for x in range(game.size_x):
        for y in range(game.size_y):
            if game.map[x][y] == 0:
                result_2 += reachable_trails[x][y]

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
    global path
    path = "day-" + str(day).zfill(2) + "/"

    test_sol_1 = ["36"]
    test_sol_2 = ["81"]

    test = True

    sol1 = sub1 = False
    sol2 = sub2 = False

    if test:
        if not run_tests(test_sol_1, test_sol_2, path):
            sub1 = sub2 = False

    data_main = get_data(day=day, year=2024).splitlines()

    if sol1:
        result_1 = part_1(data_main, True)
        print("Result Part 1: " + str(result_1))

    if sol2:
        result_2 = part_2(data_main, True)
        print("Result Part 2: " + str(result_2))

    print("\n")

    if sub1:
        submit(int(result_1), part="a", day=day, year=2024)

    if sub2:
        submit(int(result_2), part="b", day=day, year=2024)


if __name__ == "__main__":
    main()
