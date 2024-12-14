import re
from aocd import submit
from aocd import get_data
import pulp
from pulp import LpProblem, PULP_CBC_CMD

import time

from importlib.machinery import SourceFileLoader

lib = SourceFileLoader("lib", "lib.py").load_module()

day = 13
path = ""

test_sol_1 = ["480"]
test_sol_2 = ["875318608908"]

sol_1 = sub_1 = False
sol_2 = sub_2 = False


class ClawMachine():

    def __init__(self, shift_a: tuple[int, int], shift_b: tuple[int, int], prize: tuple[int, int]):
        self.shift_a = shift_a
        self.shift_b = shift_b
        self.prize = prize


def parse_input(input: list[str]) -> list[ClawMachine]:

    machines = []

    num = re.compile(r'\d+')

    for i in range(0, len(input), 4):

        shift_a = [int(val) for val in num.findall(input[i])]
        shift_b = [int(val) for val in num.findall(input[i+1])]
        prize = [int(val) for val in num.findall(input[i+2])]
        machines.append(ClawMachine(shift_a, shift_b, prize))

    return machines


def scale_prize(machine: ClawMachine, additive_term: int) -> ClawMachine:

    return ClawMachine(machine.shift_a, machine.shift_b, (machine.prize[0] + additive_term, machine.prize[1] + additive_term))


def evaluate_machine_part_2(machine: ClawMachine) -> int:

    # a = (b_x * p_y - b_y * p_x) / (a_y * b_x - a_x * b_y)
    a = (machine.shift_b[0] * machine.prize[1] - machine.shift_b[1] * machine.prize[0])/(
        machine.shift_a[1] * machine.shift_b[0] - machine.shift_a[0] * machine.shift_b[1])
    # b = (p_x - a_x * a) / b_x
    b = (machine.prize[0] - machine.shift_a[0] * a)/(
        machine.shift_b[0])

    return 3 * int(a) + int(b) if is_valid(int(a), int(b), machine) else 0


def is_valid(a: int, b: int, machine: ClawMachine) -> bool:

    return a * machine.shift_a[0] + b * machine.shift_b[0] == machine.prize[0] and a * machine.shift_a[1] + b * machine.shift_b[1] == machine.prize[1]


def evaluate_machine(machine: ClawMachine, max_trials: int) -> int:

    # A = press a, a_x = shift a in x, a_y = shift a in y
    # B = press b, b_x = shift b in x, b_y = shift b in y
    # p_x = prize x, p_y = prize y

    # min 3 * a + b
    # s.t.    a * a_x + b * b_x = p_x
    #         a * a_y + b * b_y = p_y
    #         a, b \in Z
    #         a, b >= 0
    #         a, b <= max_trials

    prob: LpProblem = pulp.LpProblem("claw-solver", pulp.LpMinimize)

    a = pulp.LpVariable('a', lowBound=0, upBound=max_trials, cat='Integer')
    b = pulp.LpVariable('b', lowBound=0, upBound=max_trials, cat='Integer')

    prob += 3 * a + b, "Objective"

    prob += a * machine.shift_a[0] + b * \
        machine.shift_b[0] == machine.prize[0], "x-must-match"
    prob += a * machine.shift_a[1] + b * \
        machine.shift_b[1] == machine.prize[1], "y-must-match"

    prob.solve(PULP_CBC_CMD(msg=False))

    return 0 if "Infeasible" == pulp.LpStatus[prob.status] else int(pulp.value(prob.objective))


def shift(point: tuple[int, int], delta: tuple[int, int], times: int) -> tuple[int, int]:

    return (point[0] + delta[0] * times, point[1] + delta[1] * times)


def part_1(data, measure=False):

    startTime = time.time()
    result_1 = 0

    machines = parse_input(data)
    for machine in machines:
        result_1 += evaluate_machine(machine, 100)

    execution_time = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 1 took: " + str(execution_time) + " s")
    return str(result_1)


def part_2(data, measure=False):

    startTime = time.time()
    result_2 = 0

    additive_term = 10_000_000_000_000

    machines = parse_input(data)
    for machine in machines:
        machine = scale_prize(machine, additive_term)
        result_2 += evaluate_machine_part_2(machine)

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
