from aocd import submit
from aocd import get_data
from datetime import date
import numpy as np
import time
import pprint

from importlib.machinery import SourceFileLoader

lib = SourceFileLoader("lib", "lib.py").load_module()


day = 8
path = ""


class Point():

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


class Instance():

    def __init__(self, antennas: list[Point], size_x: int, size_y: int):
        self.antennas = antennas
        self.size_x = size_x
        self.size_y = size_y


def parseInput(input: list[str]) -> dict[str, Instance]:

    result: dict[str, Instance] = dict()

    size_x = len(input[0])
    size_y = len(input)

    for y in range(len(input)):
        for x in range(len(input[y])):
            char = input[y][x]
            if char != ".":
                antennas = []
                if char in result:
                    antennas = result[char].antennas
                antennas.append(Point(x, y))
                result[char] = Instance(antennas, size_x, size_y)

    return result


def get_all_antinodes(instance: Instance, is_part_2: bool) -> list[Point]:

    antinodes: set[Point] = set()

    for i in range(len(instance.antennas)-1):
        for j in range(i + 1, len(instance.antennas)):
            for antinode in get_antinodes(instance.antennas[i], instance.antennas[j], instance):
                antinodes.add(antinode)
            if is_part_2:
                for antinode in get_additional_antinodes(instance.antennas[i], instance.antennas[j], instance):
                    antinodes.add(antinode)

    return antinodes


def get_antinodes(antenna_a: Point, antenna_b: Point, instance: Instance) -> list[Point]:

    a_to_b = Point(antenna_b.x - antenna_a.x, antenna_b.y - antenna_a.y)
    candidates = [
        Point(antenna_a.x - a_to_b.x, antenna_a.y - a_to_b.y),
        Point(antenna_b.x + a_to_b.x, antenna_b.y + a_to_b.y)
    ]

    if float(antenna_b.x) - (float(a_to_b.x) * (float(2)/float(3))) % 1 == 0 and float(antenna_b.y) - (float(a_to_b.y) * (float(2)/float(3))) % 1 == 0:
        candidates.append(Point(float(antenna_b.x) - (float(a_to_b.x) * (float(2)/float(3))),
                          float(antenna_b.y) - (float(a_to_b.y) * (float(2)/float(3)))))

    if float(antenna_b.x) - (float(a_to_b.x) * (float(1)/float(3))) % 1 == 0 and float(antenna_b.y) - (float(a_to_b.y) * (float(1)/float(3))) % 1 == 0:
        candidates.append(Point(float(antenna_b.x) - (float(a_to_b.x) * (float(1)/float(3))),
                          float(antenna_b.y) - (float(a_to_b.y) * (float(1)/float(3)))))

    valid_candidates = []
    for candidate in candidates:
        if is_inside(candidate, instance.size_x, instance.size_y):
            valid_candidates.append(candidate)

    return valid_candidates


def get_additional_antinodes(antenna_a: Point, antenna_b: Point, instance: Instance) -> list[Point]:

    a_to_b = Point(antenna_b.x - antenna_a.x, antenna_b.y - antenna_a.y)
    antinodes = []

    current_node = Point(antenna_a.x, antenna_a.y)
    while is_inside(current_node, instance.size_x, instance.size_y):
        antinodes.append(current_node)
        current_node = Point(current_node.x - a_to_b.x,
                             current_node.y - a_to_b.y)

    current_node = Point(antenna_b.x, antenna_b.y)
    while is_inside(current_node, instance.size_x, instance.size_y):
        antinodes.append(current_node)
        current_node = Point(current_node.x + a_to_b.x,
                             current_node.y + a_to_b.y)

    return antinodes


def is_inside(point: Point, size_x: int, size_y: int) -> bool:

    return point.x >= 0 and point.x < size_x and point.y >= 0 and point.y < size_y


def print_all(instances: dict[str, Instance], antinodes: set[Point]) -> None:

    first = next(iter(instances.values()))

    field = [["." for x in range(first.size_x)] for y in range(first.size_y)]

    for antinode in antinodes:
        field[antinode.y][antinode.x] = "#"

    for typ, instance in instances.items():
        for antenna in instance.antennas:
            field[antenna.y][antenna.x] = typ

    for y in range(len(field)):
        line = "".join(field[y])
        print(line)


def part1(data, measure=False):
    startTime = time.time()
    antinodes = set()

    instances = parseInput(data)

    for instance in instances.values():
        for antinode in get_all_antinodes(instance, False):
            antinodes.add(antinode)

    # print_all(instances, antinodes)

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 1 took: " + str(executionTime) + " s")
    return str(len(antinodes))


def part2(data, measure=False):
    startTime = time.time()
    antinodes = set()

    instances = parseInput(data)

    for instance in instances.values():
        for antinode in get_all_antinodes(instance, True):
            antinodes.add(antinode)

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 2 took: " + str(executionTime) + " s")
    return str(len(antinodes))


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

    test_sol_1 = ["14"]
    test_sol_2 = ["34"]

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
