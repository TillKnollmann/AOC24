import os


def get_data_lines(path: str) -> list:
    with open(path, "r") as file:
        lines = file.readlines()
    lines = [lines[i].replace("\n", "") for i in range(0, len(lines))]
    return lines


def get_test_paths(path) -> list:
    paths = []
    for root, dirs, files in os.walk(path):
        files.sort()
        # select file name
        for file in files:
            # check the extension of files
            if file.endswith(".txt"):
                # print whole path of files
                paths.append(os.path.join(root, file))
    return paths
