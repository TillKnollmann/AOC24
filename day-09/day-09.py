import math
from aocd import submit
from aocd import get_data
from datetime import date
import numpy as np
import time
import pprint

from importlib.machinery import SourceFileLoader

lib = SourceFileLoader("lib", "lib.py").load_module()


day = 9
path = ""


class Block():

    def __init__(self, is_free: bool, size: int, id: int):
        self.is_free = is_free
        self.size = size
        self.id = id


def parse_input(input: list[str]) -> list[Block]:

    result = []

    file_id = 0
    is_file = True
    for block in input[0]:
        if is_file:
            result.append(Block(False, int(block), file_id))
            file_id += 1
        else:
            result.append(Block(True, int(block), -1))
        is_file = not is_file

    return result


def get_checksum(blocks: list[Block]) -> int:

    position: int = 0
    checksum: int = 0

    while len(blocks) > 0:

        current = blocks.pop(0)
        if not current.is_free:
            checksum += get_block_checksum(position, current.size, current.id)
        position += current.size

    return checksum


def get_block_checksum(position: int, size: int, identifier: int) -> int:

    # checksum is position * size * identifier + (((size - 1)^2 + size - 1) / 2) * identifier
    return int(position * size * identifier + ((math.pow(size - 1, 2) + size - 1) / 2) * identifier)


def fill_free_space_part_1(blocks: list[Block]) -> list[Block]:

    filled: list[Block] = []

    while len(blocks) > 0:
        first_block = blocks.pop(0)
        if not first_block.is_free:
            filled.append(first_block)  # append file
        else:
            while first_block.size > 0 and len(blocks) > 0:
                # (partially) append last file
                last_block = blocks.pop()
                used_size = min(first_block.size, last_block.size)
                filled.append(Block(False, used_size, last_block.id))
                # reduce sizes of free space/last file
                first_block.size -= used_size
                last_block.size -= used_size
                if last_block.size > 0:
                    # last file was not used completely
                    blocks.append(last_block)
                else:
                    if len(blocks) > 0:
                        blocks.pop()  # last file was used completely -> remove last free space

    return filled


def fill_free_space_part_2(blocks: list[Block]) -> list[Block]:

    disk = [block for block in blocks]

    files_reversed = []
    for i in reversed(range(len(blocks))):
        if not blocks[i].is_free:
            files_reversed.append(blocks[i])

    for file in files_reversed:
        disk = move_block(disk, file)

    return disk


def move_block(disk: list[Block], considered_block: Block) -> list[Block]:

    new_disk = []

    considered_inserted = False

    for block in disk:
        if block.id == considered_block.id:
            if considered_inserted:
                new_disk.append(Block(True, block.size, -1))
            else:
                new_disk.append(block)
                considered_inserted = True
        elif considered_inserted:
            new_disk.append(block)
        elif not block.is_free:
            new_disk.append(block)
        elif block.size < considered_block.size:
            new_disk.append(block)
        else:
            new_disk.append(considered_block)
            considered_inserted = True
            if block.size > considered_block.size:
                new_disk.append(
                    Block(True, block.size - considered_block.size, -1))

    return new_disk


def print_disk(blocks: list[Block]) -> None:

    dist = []
    for block in blocks:
        if block.is_free:
            dist.append("".join(["." for i in range(block.size)]))
        else:
            dist.append("".join([str(block.id) for i in range(block.size)]))

    print("".join(dist))


def part_1(data, measure=False):
    startTime = time.time()
    result_1 = None

    disk = parse_input(data)
    # print_disk(disk)

    disk_filled = fill_free_space_part_1(disk)
    # print_disk(disk_filled)

    result_1 = get_checksum(disk_filled)

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 1 took: " + str(executionTime) + " s")
    return str(result_1)


def part_2(data, measure=False):
    startTime = time.time()
    result_2 = None

    disk = parse_input(data)
    # print_disk(disk)

    disk_filled = fill_free_space_part_2(disk)
    # print_disk(disk_filled)

    result_2 = get_checksum(disk_filled)

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

    test_sol_1 = ["1928"]
    test_sol_2 = ["2858"]

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
