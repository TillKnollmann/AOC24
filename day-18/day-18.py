from aocd import submit
from aocd import get_data

import heapq

import time

from importlib.machinery import SourceFileLoader

lib = SourceFileLoader("lib", "lib.py").load_module()

day = 18
path = ""

test_sol_1 = ["22"]
test_sol_2 = ["6,1"]

sol_1 = sub_1 = True
sol_2 = sub_2 = True


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

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)


def parse_input(input: list[str], field_size: Point) -> tuple[list[Point], list[list[int]]]:

    points = []
    field = [[0 for _ in range(field_size.y + 1)] for _ in range(field_size.x + 1)]

    for line in input:
        line = line.strip()
        x, y = map(int, line.split(","))
        points.append(Point(x, y))

    return points, field

def build_field(points_subset: list[Point], field_size: Point) -> list[list[int]]:
    field = [[0 for _ in range(field_size.y + 1)] for _ in range(field_size.x + 1)]
    for point in points_subset:
        field = set_field_value(field, point)
    return field

def set_field_value(field: list[list[int]], point: Point) -> list[list[int]]:
    new_field = [row[:] for row in field]  # Create a copy of the field
    new_field[point.x][point.y] = 1
    return new_field

def print_field(field: list[list[int]]) -> None:
    for row in field:
        print("".join(str(cell) for cell in row))
    print()

def dijkstra(field: list[list[int]], start: Point, end: Point) -> int:
    rows, cols = len(field), len(field[0])
    distances = [[float('inf')] * cols for _ in range(rows)]
    distances[start.x][start.y] = 0
    priority_queue = [(0, start)]  # (distance, Point)

    directions = [Point(0, 1), Point(1, 0), Point(0, -1), Point(-1, 0)]  # right, down, left, up

    while priority_queue:
        current_distance, current_point = heapq.heappop(priority_queue)

        if current_point == end:
            return current_distance

        if current_distance > distances[current_point.x][current_point.y]:
            continue

        for direction in directions:
            neighbor = Point(current_point.x + direction.x, current_point.y + direction.y)

            if 0 <= neighbor.x < rows and 0 <= neighbor.y < cols and field[neighbor.x][neighbor.y] == 0:
                new_distance = current_distance + 1

                if new_distance < distances[neighbor.x][neighbor.y]:
                    distances[neighbor.x][neighbor.y] = new_distance
                    heapq.heappush(priority_queue, (new_distance, neighbor))

    return -1  # Return -1 if no path exists

def reachable(field: list[list[int]], start: Point, end: Point) -> bool:
    rows, cols = len(field), len(field[0])
    visited = [[False] * cols for _ in range(rows)]
    return dfs(field, start, end, visited)

def dfs(field: list[list[int]], current: Point, end: Point, visited: list[list[bool]]) -> bool:
    rows, cols = len(field), len(field[0])

    if current == end:
        return True
    if not (0 <= current.x < rows and 0 <= current.y < cols) or field[current.x][current.y] == 1 or visited[current.x][current.y]:
        return False

    visited[current.x][current.y] = True

    directions = [Point(0, 1), Point(1, 0), Point(0, -1), Point(-1, 0)]  # right, down, left, up
    for direction in directions:
        neighbor = Point(current.x + direction.x, current.y + direction.y)
        if dfs(field, neighbor, end, visited):
            return True

    return False

def part_1(data, measure=False, test=False):

    startTime = time.time()
    result_1 = None

    field_size = Point(70, 70) if not test else Point(6, 6)
    length = 1024 if not test else 12
    points, field = parse_input(data, field_size)

    for i in range(length):
        field = set_field_value(field, points[i])

    result_1 = dijkstra(field, Point(0, 0), Point(field_size.x, field_size.y))

    execution_time = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 1 took: " + str(execution_time) + " s")
    return str(result_1)


def part_2(data, measure=False, test=False):

    startTime = time.time()
    result_2 = None

    field_size = Point(70, 70) if not test else Point(6, 6)
    points, field = parse_input(data, field_size)

    left, right = 0, len(points) - 1
    result_2 = None

    while left <= right:
        mid = (left + right) // 2
        field = build_field(points[:mid + 1], field_size)
        if not reachable(field, Point(0, 0), field_size):
            result_2 = f"{points[mid].x},{points[mid].y}"
            right = mid - 1
        else:
            left = mid + 1

    execution_time = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 2 took: " + str(execution_time) + " s")
    return str(result_2)


def run_tests(test_sol_1, test_sol_2, path):

    test_res_1 = []
    test_res_2 = []

    all_check = True

    paths = lib.get_test_paths(path)

    test_res_1 += list(map(part_1, map(lib.get_data_lines, paths), [False] * len(paths), [True] * len(paths)))
    test_res_2 += list(map(part_2, map(lib.get_data_lines, paths), [False] * len(paths), [True] * len(paths)))

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
        result_1 = part_1(data_main, True, False)
        print("Result Part 1: " + str(result_1))

    if sol_2:
        result_2 = part_2(data_main, True, False)
        print("Result Part 2: " + str(result_2))

    print("\n")

    if sub_1:
        submit(result_1, part="a", day=day, year=2024)

    if sub_2:
        submit(result_2, part="b", day=day, year=2024)


if __name__ == "__main__":
    main()
