import copy
import operator
import re
from aocd import submit
from aocd import get_data

import time
import numpy as np

from consoledraw import Console

from importlib.machinery import SourceFileLoader

lib = SourceFileLoader("lib", "lib.py").load_module()

day = 14
path = ""

test_sol_1 = ["12"]
test_sol_2 = []  # No tests for part 2

sol_1 = sub_1 = False
sol_2 = sub_2 = False
sol_2 = True


class Robot:

    def __init__(self, vel: tuple[int, int], pos: tuple[int, int]):
        self.vel = vel
        self.pos = pos


class Game:

    def __init__(self, size_x: int, size_y: int, bots: list[Robot]):
        self.size_x = size_x
        self.size_y = size_y
        self.bots = bots


def parse_input(input: list[str]):

    num_pat = re.compile(r'-?\d+')

    size_x = 101
    size_y = 103

    if input[0] == "p=0,4 v=3,-3":
        # test case
        size_x = 11
        size_y = 7

    bots = []

    for line in input:
        nums = [int(num) for num in num_pat.findall(line)]
        bots.append(Robot((nums[2], nums[3]), (nums[0], nums[1])))

    return Game(size_x, size_y, bots)


def simulate_robot(bot: Robot, game: Game, runs: int) -> Robot:

    new_x = bot.pos[0] + runs * bot.vel[0]
    new_y = bot.pos[1] + runs * bot.vel[1]

    new_x = new_x % game.size_x
    new_y = new_y % game.size_y

    return Robot(bot.vel, (new_x, new_y))


def evaluate_game(game: Game) -> tuple[np.array, np.array, np.array, np.array]:

    field: np.array = np.zeros(shape=(game.size_x, game.size_y))
    for bot in game.bots:
        field[bot.pos[0]][bot.pos[1]] += 1

    field = np.delete(field, int(game.size_x/2), 0)
    field = np.delete(field, int(game.size_y/2), 1)

    upper, lower = np.vsplit(field, 2)
    q1, q2 = np.hsplit(upper, 2)
    q3, q4 = np.hsplit(lower, 2)

    return q1, q2, q3, q4


def print_game(game: Game) -> None:

    field = [["." for y in range(game.size_y)] for x in range(game.size_x)]
    for bot in game.bots:
        field[bot.pos[0]][bot.pos[1]] = "#"

    for y in range(game.size_y):
        print("".join([field[x][y] for x in range(game.size_x)]))


def part_1(data, measure=False):

    startTime = time.time()
    result_1 = 0

    game: Game = parse_input(data)

    new_bots = []

    for bot in game.bots:
        new_bots.append(simulate_robot(bot, game, 100))

    q1, q2, q3, q4 = evaluate_game(Game(game.size_x, game.size_y, new_bots))
    result_1 = int(q1.sum() * q2.sum() * q3.sum() * q4.sum())

    execution_time = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 1 took: " + str(execution_time) + " s")
    return str(result_1)


def part_2(data, measure=False):

    startTime = time.time()

    result_2 = 0

    game: Game = parse_input(data)

    limit = 10_000
    seconds = 0

    safeties = []

    for seconds in range(1, limit):
        new_bots = []
        for bot in game.bots:
            new_bots.append(simulate_robot(bot, game, seconds))
        q1, q2, q3, q4 = evaluate_game(
            Game(game.size_x, game.size_y, new_bots))
        safeties.append(
            (int(q1.sum() * q2.sum() * q3.sum() * q4.sum()), seconds))

    for item in sorted(safeties, key=operator.itemgetter(0)):
        new_bots = []
        for bot in game.bots:
            new_bots.append(simulate_robot(bot, game, item[1]))
        print()
        print_game(Game(game.size_x, game.size_y, new_bots))
        if "y" == input("Tree? (y,n)"):
            result_2 = item[1]
            break

    execution_time = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 2 took: " + str(execution_time) + " s")
    return str(result_2)


def run_tests(test_sol_1, test_sol_2, path):

    test_res_1 = []

    all_check = True

    paths = lib.get_test_paths(path)

    test_res_1 += list(map(part_1, map(lib.get_data_lines, paths)))

    success_1 = [(test_sol_1[i] == test_res_1[i])
                 for i in range(len(test_sol_1))]

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
