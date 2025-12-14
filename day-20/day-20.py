import time
from importlib.machinery import SourceFileLoader
from itertools import product

from aocd import get_data
from aocd import submit

lib = SourceFileLoader("lib", "../lib.py").load_module()

day = int("20")
path = ""

test_sol_1 = ["0"]
test_sol_2 = ["0"]

sol_1 = sub_1 = True
sol_2 = sub_2 = True


def parse_input(input_lines: list[str]) -> list[tuple[int, int]]:
    """Returns the unique path as a list of coordinates from start to stop"""
    max_x = len(input_lines[0])
    max_y = len(input_lines)

    start_character: str = 'S'
    stop_character: str = 'E'
    wall_character: str = '#'

    race_path: list[tuple[int, int]] = []

    for y, line in enumerate(input_lines):
        for x, character in enumerate(line):
            if character == start_character:
                race_path.append((x, y))
                break

    stop_reached: bool = False
    offsets: list[tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while not stop_reached:
        next_position: tuple[int, int]
        for next_position in [tuple(map(sum, zip(race_path[-1], b))) for b in offsets]:
            if 0 <= next_position[0] < max_x and 0 <= next_position[1] < max_y:
                if len(race_path) < 2 or next_position != race_path[-2]:
                    if input_lines[next_position[1]][next_position[0]] != wall_character:
                        race_path.append(next_position)
                        if input_lines[next_position[1]][next_position[0]] == stop_character:
                            stop_reached = True
                        break

    return race_path


def part_1(data, measure=False):
    start_time = time.time()

    max_distance: int = 2

    race_path: list[tuple[int, int]] = parse_input(data)
    weight_by_position: dict[tuple[int, int], int] = dict()
    for index, position in enumerate(race_path):
        weight_by_position[position] = index

    weighted_shortcuts: set[tuple[tuple[int, int], tuple[int, int], int]] = set()
    for position in weight_by_position.keys():
        for weighted_shortcut in get_weighted_cheats(weight_by_position, position, max_distance):
            weighted_shortcuts.add(weighted_shortcut)

    result_part_1 = len(list(filter(lambda x: x[2] >= 100, weighted_shortcuts)))

    execution_time = round(time.time() - start_time, 2)
    if measure:
        print("\nPart 1 took: " + str(execution_time) + " s")
    return str(result_part_1)


def part_2(data, measure=False):
    start_time = time.time()

    max_distance: int = 20

    race_path: list[tuple[int, int]] = parse_input(data)
    weight_by_position: dict[tuple[int, int], int] = dict()
    for index, position in enumerate(race_path):
        weight_by_position[position] = index

    weighted_shortcuts: set[tuple[tuple[int, int], tuple[int, int], int]] = set()
    for position in weight_by_position.keys():
        for weighted_shortcut in get_weighted_cheats(weight_by_position, position, max_distance):
            weighted_shortcuts.add(weighted_shortcut)

    result_part_2 = len(list(filter(lambda x: x[2] >= 100, weighted_shortcuts)))

    execution_time = round(time.time() - start_time, 2)
    if measure:
        print("\nPart 2 took: " + str(execution_time) + " s")
    return str(result_part_2)


def get_weighted_cheats(weight_by_position: dict[tuple[int, int], int], position: tuple[int, int], max_distance: int) -> \
set[tuple[tuple[int, int], tuple[int, int], int]]:
    cheats = get_cheats(weight_by_position, position, max_distance)
    weighted_cheats: set[tuple[tuple[int, int], tuple[int, int], int]] = set()
    for cheat in cheats:
        weight: int = weight_by_position[cheat[1]] - weight_by_position[cheat[0]] - abs(
            cheat[1][0] - cheat[0][0]) - abs(cheat[1][1] - cheat[0][1])
        if weight > 0:
            weighted_cheats.add((cheat[0], cheat[1], weight))
    return weighted_cheats


def get_cheats(weight_by_position: dict[tuple[int, int], int], position: tuple[int, int], max_distance: int) -> set[
    tuple[tuple[int, int], tuple[int, int]]]:
    cheats: set[tuple[tuple[int, int], tuple[int, int]]] = set()
    offsets = get_offsets(max_distance)
    next_position: tuple[int, int]
    for next_position in [tuple(map(sum, zip(position, b))) for b in offsets]:
        if next_position in weight_by_position and weight_by_position[next_position] > weight_by_position[position]:
            cheats.add((position, next_position))
    return cheats


def get_offsets(max_distance: int) -> list[tuple[int, int]]:
    ranges: list[int] = [i for i in range(-max_distance, max_distance + 1)]
    offsets: list[tuple[int, int]] = list(product(ranges, ranges))
    offsets = list(filter(lambda x: 0 < abs(x[0]) + abs(x[1]) <= max_distance, offsets))
    return offsets


def run_tests(test_solution_1, test_solution_2, day_path):
    test_res_1 = []
    test_res_2 = []

    all_check = True

    paths = lib.get_test_paths(day_path)

    test_res_1 += list(map(part_1, map(lib.get_data_lines, paths)))
    test_res_2 += list(map(part_2, map(lib.get_data_lines, paths)))

    success_1 = [(test_solution_1[i] == test_res_1[i])
                 for i in range(len(test_solution_1))]
    success_2 = [(test_solution_2[i] == test_res_2[i])
                 for i in range(len(test_solution_2))]

    for i in range(len(test_solution_1)):
        if success_1[i]:
            print("Part 1 Test " + str(i + 1) + " Succeeded!")
        else:
            print(
                "Part 1 Test "
                + str(i + 1)
                + " Failed! Expected "
                + str(test_solution_1[i])
                + " received "
                + test_res_1[i]
            )
            all_check = False

    print()

    for i in range(len(test_solution_2)):
        if success_2[i]:
            print("Part 2 Test " + str(i + 1) + " Succeeded!")
        else:
            print(
                "Part 2 Test "
                + str(i + 1)
                + " Failed! Expected "
                + str(test_solution_2[i])
                + " received "
                + test_res_2[i]
            )
            all_check = False

    return all_check


def main():
    global path, sol_1, sol_2, sub_1, sub_2
    path = "../day-" + str(day).zfill(2) + "/"

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

    if sol_1 and sub_1:
        submit(int(result_1), part="a", day=day, year=2024)

    if sol_2 and sub_2:
        submit(int(result_2), part="b", day=day, year=2024)


if __name__ == "__main__":
    main()
