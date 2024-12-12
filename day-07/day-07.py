import re
from enum import Enum
from aocd import submit
from aocd import get_data
from datetime import date
import numpy as np
import time
import pprint

from importlib.machinery import SourceFileLoader

lib = SourceFileLoader("lib", "lib.py").load_module()


day = 7
path = ""


class Operator(Enum):
    ADD = 1
    MULT = 2
    CONCAT = 3


class Instance:
    def __init__(self, result: int, values: list[int]):
        self.result = result
        self.values = values


def parse_input(input: list[str]) -> list[Instance]:

    num_pattern = re.compile(r'\d+')

    output = []

    for line in input:
        result_string = line.split(":")[0]
        values_string = line.split(":")[1]
        result = int(result_string)
        values = [int(num) for num in num_pattern.findall(values_string)]
        output.append(Instance(result, values))

    return output


def can_instance_be_true_part_1(instance: Instance) -> bool:

    return is_instance_true_part_1(instance, instance.values[0], [])


def is_instance_true_part_1(instance: Instance, current_value: int, current_operators: list[Operator]) -> bool:

    if len(current_operators) == len(instance.values) - 1:
        return instance.result == current_value

    return is_instance_true_part_1(instance, evaluate(current_value, instance.values[len(current_operators) + 1], Operator.ADD), current_operators + [Operator.ADD]) or is_instance_true_part_1(instance, evaluate(current_value, instance.values[len(current_operators) + 1], Operator.MULT), current_operators + [Operator.MULT])


def can_instance_be_true_part_2(instance: Instance) -> bool:

    return is_instance_true_part_2(instance, instance.values[0], [])


def is_instance_true_part_2(instance: Instance, current_value: int, current_operators: list[Operator]) -> bool:

    if len(current_operators) == len(instance.values) - 1:
        return instance.result == current_value

    if current_value > instance.result:
        return False

    return is_instance_true_part_2(instance, evaluate(current_value, instance.values[len(current_operators) + 1], Operator.ADD), current_operators + [Operator.ADD]) or is_instance_true_part_2(instance, evaluate(current_value, instance.values[len(current_operators) + 1], Operator.MULT), current_operators + [Operator.MULT]) or is_instance_true_part_2(instance, evaluate(current_value, instance.values[len(current_operators) + 1], Operator.CONCAT), current_operators + [Operator.CONCAT])


def evaluate(value_a: int, value_b: int, operator: Operator) -> int:

    match operator:
        case Operator.ADD:
            return value_a + value_b
        case Operator.MULT:
            return value_a * value_b
        case Operator.CONCAT:
            return int(str(value_a) + str(value_b))


def part_1(data, measure=False):
    startTime = time.time()
    result_1 = 0

    instances = parse_input(data)

    for instance in instances:
        if can_instance_be_true_part_1(instance):
            result_1 += instance.result

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 1 took: " + str(executionTime) + " s")
    return str(result_1)


def part_2(data, measure=False):
    startTime = time.time()
    result_2 = 0

    instances = parse_input(data)

    for instance in instances:
        if can_instance_be_true_part_2(instance):
            result_2 += instance.result

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

    test_sol_1 = ["3749"]
    test_sol_2 = ["11387"]

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
