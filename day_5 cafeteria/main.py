import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils import read_lines
from collections import namedtuple

SAMPLE_INPUT = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""

Range = namedtuple('Range', 'lower upper')

def solve_puzzle():
    # Read the input
    # input_data = SAMPLE_INPUT.split()
    input_data = read_lines(__file__)

    # part one
    ranges = []
    ingredient_ids = []
    for line in input_data:
        if '-' in line:
            lower, upper = line.split('-')
            ranges.append(Range(int(lower), int(upper)))
        elif line:
            ingredient_ids.append(int(line))

    fresh = 0
    for ingredient_id in ingredient_ids:
        for ig_range in ranges:
            if ig_range.lower <= ingredient_id <= ig_range.upper:
                fresh += 1
                break

    print(f"There are {fresh} fresh ingredients")

    # part two
    sorted_by_lower = sorted(ranges, key=lambda x: x.lower, reverse=True)
    current_lower = current_upper = None

    fresh_range = 0

    while sorted_by_lower:
        r = sorted_by_lower.pop()
        if current_lower is None:
            current_lower, current_upper = r
        elif current_upper >= r.lower:
            current_upper = max(current_upper, r.upper)
        else:
            fresh_range += (current_upper - current_lower + 1)
            current_lower, current_upper = r

    fresh_range += (current_upper - current_lower + 1)
    print(f"A total of {fresh_range} are considered to be fresh")

    

if __name__ == "__main__":
    solve_puzzle()