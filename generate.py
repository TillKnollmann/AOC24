import os
import shutil
import argparse

tab = "    "


def main():
    parser = argparse.ArgumentParser(
        description="Generator for AOC day solutions")
    parser.add_argument('-d', '--day', type=int,
                        help='The day to generate', required=True)
    args = parser.parse_args()

    path = os.getcwd()
    template_path = os.path.join(path, "template")
    current_path = os.path.join(path, "day-" + str(args.day))
    if not os.path.exists(current_path):
        shutil.copytree(template_path, current_path)
        day_name = "day-" + str(args.day) + ".py"
        os.rename(
            str(current_path) + "/template.py", str(current_path) + "/" + day_name
        )
        file_data = ""
        with open(current_path + "/" + day_name, "r") as file:
            file_data = file.read()
        file_data = file_data.replace("DAY", str(args.day))
        with open(current_path + "/" + day_name, "w") as file:
            file.write(file_data)


if __name__ == "__main__":
    main()
