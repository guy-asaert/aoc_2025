import copy
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils import read_lines
from collections import namedtuple

SAMPLE_INPUT = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""


OFFSETS = (
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
    (1, 0),
    (1, -1),
    (0, -1)
)


def solve(part2: bool = False):
    # Read the input
    grid_data = read_lines(__file__)
    # grid_data = SAMPLE_INPUT.split()

    grid = []
    for data_row in grid_data:
        grid.append(['.'] + list(data_row) + ['.'])
    
    grid.insert(0, '.' * len(grid[0]))
    grid.append('.' * len(grid[0]))
    
    total_removed = 0
    removed_roll = -1

    while removed_roll != 0:
        print()
        removed_roll = 0
        current_grid = copy.deepcopy(grid)
        for row in range(1, len(current_grid) - 1):
            for col in range(1, len(current_grid[0]) - 1):
                if current_grid[row][col] != '@':
                    print(current_grid[row][col], end='')
                    continue
                adjacent_paper = 0
                for row_offset, col_offset in OFFSETS:
                    if current_grid[row - row_offset][col - col_offset] == '@':
                        adjacent_paper += 1
                if adjacent_paper < 4: # remove paper roll
                    grid[row][col] = '.'
                    removed_roll += 1
                    print('x', end='')
                else:
                    print(grid[row][col], end='')
            print()
        total_removed += removed_roll
        if not part2:
            break

    print()
    for row in range(1, len(current_grid) - 1):
        for col in range(1, len(current_grid[0]) - 1):
            print(current_grid[row][col], end='')
        print()
    print()

    print(f"{total_removed} were removed")


if __name__ == "__main__":
    solve(part2=True)
