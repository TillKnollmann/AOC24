from aocd import submit
from aocd import get_data

import time
import numpy as np
from tqdm import tqdm
from consoledraw import Console

from importlib.machinery import SourceFileLoader

lib = SourceFileLoader("lib", "../lib.py").load_module()

day = 15
path = ""

test_sol_1 = ["2028", "10092"]
test_sol_2 = ["", "9021"]

sol_1 = sub_1 = False
sol_2 = sub_2 = True  # Todo

visualize = False


class Game:

    def __init__(self, field: np.char.chararray, commands: str):
        self.field = field
        self.commands = commands


def parse_input(input: list[str]) -> Game:

    total = "\n".join(input)

    field_str, command_str = total.split("\n\n")
    field_str = field_str.split("\n")

    field = np.char.chararray(shape=(len(field_str[0]), len(field_str)))
    for y in range(len(field_str)):
        for x in range(len(field_str[0])):
            field[x][y] = field_str[y][x]

    commands = command_str.replace("\n", "")

    return Game(field, commands)


def print_game(console: Console, game: Game) -> None:

    console.clear()

    out = [["." for x in range(len(game.field))]
           for y in range(len(game.field[0]))]

    for x in range(len(game.field)):
        for y in range(len(game.field[0])):
            out[y][x] = str(game.field[x][y]).replace("'", "").replace("b", "")

    for y in range(len(out)):
        console.print("".join([char for char in out[y]]))

    console.update()


def simulate_game(game: Game) -> Game:

    global visualize, console

    if len(game.commands) > 1000:
        visualize = False

    if visualize:
        console = Console()

    for command in tqdm(game.commands, disable=len(game.commands) <= 1000 or visualize):
        game = simulate_move(game, command)
        if visualize:
            print_game(console, game)

    return game


def simulate_move(game: Game, command: str) -> Game:

    field = game.field
    match command:
        case "^":
            field = np.rot90(field, 3)  # 90 degrees left
        case ">":
            field = np.rot90(field, 2)  # 180 degrees left
        case "v":
            field = np.rot90(field, 1)  # 270 degrees left

    field = simulate_left_move(field)
    match command:
        case "^":
            field = np.rot90(field, 1)  # 270 degrees left
        case ">":
            field = np.rot90(field, 2)  # 180 degrees left
        case "v":
            field = np.rot90(field, 3)  # 90 degrees left

    return Game(field, game.commands[1:])


def find_bot(field: np.char.chararray) -> tuple[int, int]:

    for x in range(len(field)):
        for y in range(len(field[0])):
            if field[x][y] == b'@':
                return x, y

    return -1, -1


def simulate_left_move(field: np.char.chararray) -> np.char.chararray:

    bot = find_bot(field)

    if field[bot[0] - 1][bot[1]] == b'.':
        field[bot[0] - 1][bot[1]] = b'@'
        field[bot[0]][bot[1]] = b'.'
        return field

    if field[bot[0] - 1][bot[1]] == b'#':
        return field

    # need to push
    x = bot[0] - 2
    while field[x][bot[1]] != b'#' and x >= 0:
        if field[x][bot[1]] == b'.':
            field[x][bot[1]] = b'O'
            field[bot[0] - 1][bot[1]] = b'@'
            field[bot[0]][bot[1]] = b'.'
            return field
        x -= 1

    # cannot push
    return field


def evaluate_game(game: Game) -> int:

    result = 0

    for x in range(len(game.field)):
        for y in range(len(game.field[0])):
            if game.field[x][y] == b'O':
                result += get_gps(x, y)

    return result


def get_gps(x: int, y: int) -> int:

    return x + 100 * y


def part_1(data, measure=False):

    startTime = time.time()
    result_1 = None

    game = parse_input(data)

    game = simulate_game(game)

    result_1 = evaluate_game(game)

    execution_time = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 1 took: " + str(execution_time) + " s")
    return str(result_1)


def part_2(data, measure=False):

    startTime = time.time()
    result_2 = None

    input = parse_input(data)

    # Todo program part 2

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
    global path, sol_1, sol_2, sub_1, sub_2, result_2, result_1
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

    if sub_1:
        submit(int(result_1), part="a", day=day, year=2024)

    if sub_2:
        submit(int(result_2), part="b", day=day, year=2024)


if __name__ == "__main__":
    main()
