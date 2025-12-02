import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils import read_lines
from collections import namedtuple

SAMPLE_INPUT = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""

Rotation = namedtuple("Rotation", ["direction", "count"])

def part1_and_part2():
    # Read the input
    lines = read_lines(__file__)
    # lines = SAMPLE_INPUT.split("\n")

    rotations = []
    for line in lines:
        rotations.append(Rotation(line[0], int(line[1:])))

    first_password = 0
    second_password = 0
    current_dial_position = 50
    previous_dial_position = current_dial_position

    for rotation in rotations:
        rotation_count = rotation.count
        second_password += rotation_count // 100
        rotation_count %= 100

        if rotation.direction == 'L':
            current_dial_position -= rotation_count
        else:
            current_dial_position += rotation_count

        if (current_dial_position <= 0 or current_dial_position >= 100) and \
            abs(current_dial_position) != rotation_count:

            # how many times did we pass 0
            second_password += 1

        current_dial_position %= 100

        if current_dial_position == 0:
            first_password += 1

        previous_dial_position = current_dial_position
        # print(f"Position: {current_dial_position}")

    print(f"First Password is {first_password}")
    print(f"Second Password is {second_password}")


if __name__ == "__main__":
    part1_and_part2()
