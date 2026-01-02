import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils import read_lines
import math
import re

SAMPLE_INPUT = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +"""


def solve_puzzle_part1():
    # Read the input
    # input_data = SAMPLE_INPUT.split('\n')
    input_data = read_lines(__file__)

    NUMBER_PATTERN = r'\d+'
    OPERATOR_PATTERN = r"[+*]"

    data = []
    for line in input_data:
        number_line = [int(n) for n in re.findall(NUMBER_PATTERN, line)]
        operator_line = re.findall(OPERATOR_PATTERN, line)

        data.append(number_line if number_line else operator_line)
    
    grand_total = 0
    for problem in zip(*data):
        operator = problem[-1]
        if operator == '+':
            grand_total += sum(problem[:-1])
        else:
            grand_total += math.prod(problem[:-1])
    
    print(f"Grand total is {grand_total}")


def solve_puzzle_part2():

    # input_data = SAMPLE_INPUT.split('\n')
    input_data = read_lines(__file__)

    max_line_length = 0
    for line in input_data:
        max_line_length = max(max_line_length, len(line))

    grand_total = 0
    numbers_for_math_problem = []
    number = ''
    for col in range(max_line_length - 1, -1, -1):
        if number:
            numbers_for_math_problem.append(int(number))
            number = ''
        for line in input_data:
            if col < len(line):
                character = line[col]
                if character in "+*":
                    if number:
                        numbers_for_math_problem.append(int(number))
                        number = ''
                    if character == "+":
                        grand_total += sum(numbers_for_math_problem)
                    elif character == '*':
                        grand_total += math.prod(numbers_for_math_problem)
                    numbers_for_math_problem = []
                elif re.match(r'\d', character):
                    number += line[col]

    print(f"Grand total is {grand_total}")


if __name__ == "__main__":
    solve_puzzle_part2()