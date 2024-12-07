from datetime import date
import numpy as np
import time
import pprint

from importlib.machinery import SourceFileLoader

lib = SourceFileLoader("lib", "lib.py").load_module()

from aocd import get_data
from aocd import submit

import collections

from enum import Enum
import copy
from tqdm import tqdm

class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4

class Agent:
    def __init__(self, x: int, y: int, direction: Direction):
        self.x = x
        self.y = y
        self.direction = direction

class Field:
    def __init__(self, obstacles: dict[dict[bool]], size_x: int, size_y: int):
        self.obstacles = obstacles
        self.size_x = size_x
        self.size_y = size_y

day = 6
path = ""


def parseInput(input: list[str]) -> tuple[Agent, Field]:

    obstacles = collections.defaultdict(dict)
    start_position = None


    for y in range(len(input)):
        for x in range(len(input[y])):
            if input[y][x] == "#":
                obstacles[x][y] = True
            elif input[y][x] == '^':
                start_position = Agent(x, y, Direction.NORTH)


    return start_position, Field(obstacles, len(input[0]), len(input))

def get_visited_positions(agent: Agent, field: Field) -> tuple[list[Agent],set[tuple[int, int]]]:

    visited_positions = set()
    path = []
    current_agent = agent

    while is_agent_in_bounds(current_agent, field):

        visited_positions.add((current_agent.x, current_agent.y))
        path.append(Agent(current_agent.x, current_agent.y, current_agent.direction))
        new_agent = get_next_position(current_agent, field)
        # print(f'({current_agent.x},{current_agent.y}) -> ({new_agent.x},{new_agent.y})')
        current_agent = new_agent

    return path, visited_positions

def has_loop(agent: Agent, field: Field) -> bool:

    visited_positions = set()
    current_agent = agent

    while is_agent_in_bounds(current_agent, field) and not (current_agent.x, current_agent.y, current_agent.direction) in visited_positions:

        visited_positions.add((current_agent.x, current_agent.y, current_agent.direction))
        new_agent = get_next_position(current_agent, field)
        # print(f'({current_agent.x},{current_agent.y}) -> ({new_agent.x},{new_agent.y})')
        current_agent = new_agent

    return (current_agent.x, current_agent.y, current_agent.direction) in visited_positions

def is_agent_in_bounds(agent: Agent, field: Field) -> bool:

    return agent.x >= 0 and agent.y >= 0 and agent.x < field.size_x and agent.y < field.size_y

def get_next_position(agent: Agent, field: Field) -> Agent:

    next_agent = simulate_move(agent)
    if next_agent.x in field.obstacles and next_agent.y in field.obstacles[next_agent.x]:
        next_agent = turn_right(agent)
        next_agent = simulate_move(next_agent)

    return next_agent


def simulate_move(agent: Agent) -> Agent:

    match agent.direction:
        case Direction.NORTH:
            return Agent(agent.x, agent.y-1, agent.direction)
        case Direction.EAST:
            return Agent(agent.x+1, agent.y, agent.direction)
        case Direction.SOUTH:
            return Agent(agent.x, agent.y+1, agent.direction)
        case Direction.WEST:
            return Agent(agent.x-1, agent.y, agent.direction)


def turn_right(agent: Agent) -> Agent:

    match agent.direction:
        case Direction.NORTH:
            return Agent(agent.x, agent.y, Direction.EAST)
        case Direction.EAST:
            return Agent(agent.x, agent.y, Direction.SOUTH)
        case Direction.SOUTH:
            return Agent(agent.x, agent.y, Direction.WEST)
        case Direction.WEST:
            return Agent(agent.x, agent.y, Direction.NORTH)


def part1(data, measure=False):
    startTime = time.time()
    result_1 = None

    agent, field = parseInput(data)

    result_1 = len(get_visited_positions(agent, field)[1])

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 1 took: " + str(executionTime) + " s")
    return str(result_1)


def part2(data, measure=False):
    startTime = time.time()

    agent, field = parseInput(data)

    path, candidate_positions = get_visited_positions(agent, field)
    valid_positions = set()

    for candidate_position in tqdm(candidate_positions):
        new_obstacles = copy.deepcopy(field.obstacles)
        new_obstacles[candidate_position[0]][candidate_position[1]] = True
        new_field = Field(new_obstacles, field.size_x, field.size_y)
        if has_loop(agent, new_field):
            valid_positions.add((candidate_position[0], candidate_position[1]))

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 2 took: " + str(executionTime) + " s")
    return str(len(valid_positions))


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

    test_sol_1 = [ "41" ]
    test_sol_2 = [ "6" ]

    test = True

    sol1 = sub1 = False
    sol2 = sub2 = True  # Todo

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

