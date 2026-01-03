import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils import read_lines
from collections import namedtuple
from functools import cache


TachyonBeam = namedtuple("TachyonBeam", "x_loc y_loc")

SAMPLE_INPUT = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""

SPLITTER = '^'

def solve_puzzle_part1():
    # Read the input
    # manifold_layout = SAMPLE_INPUT.split('\n')
    manifold_layout = read_lines(__file__)

    tachyon_beams = [TachyonBeam(len(manifold_layout[0])//2, 0)]
    next_iterator_tachyon_beams = []

    keep_going = True

    number_of_splits = 0
    while keep_going:
        keep_going = False

        while tachyon_beams:
            beam = tachyon_beams.pop()
            if beam.y_loc < len(manifold_layout) - 1:
                next_loc_x = beam.x_loc
                next_loc_y = beam.y_loc + 1

                keep_going = True

                if manifold_layout[next_loc_y][next_loc_x] == SPLITTER:
                    number_of_splits += 1

                    next_iterator_tachyon_beams.append(
                        TachyonBeam(next_loc_x - 1, next_loc_y,))
                    next_iterator_tachyon_beams.append(
                        TachyonBeam(next_loc_x + 1, next_loc_y,))
                else:
                    next_iterator_tachyon_beams.append(
                        TachyonBeam(next_loc_x, next_loc_y)
                    )
            else:
                next_iterator_tachyon_beams.append(beam)

        tachyon_beams = next_iterator_tachyon_beams.copy()
        # remove dupes
        tachyon_beams = list(set(tachyon_beams))

        next_iterator_tachyon_beams.clear()
    pass

    print(f"Number of splits is {number_of_splits}")
    print(f"Number of time lines is {len(tachyon_beams)}")

@cache
def _project_beam(beam: TachyonBeam, 
                  manifold_layout: list[list]):

    beam_count = 0
    keep_going = True
    while keep_going:
        next_x = beam.x_loc
        next_y = beam.y_loc + 1

        if next_y == len(manifold_layout) - 1:
            # hit the bottom
            beam_count += 1
            keep_going = False
        elif manifold_layout[next_y][next_x] == SPLITTER:
            beam_count += _project_beam(TachyonBeam(next_x - 1, next_y), 
                                        manifold_layout)
            beam_count += _project_beam(TachyonBeam(next_x + 1, next_y), 
                                        manifold_layout)
            keep_going = False
        else:
            beam = TachyonBeam(next_x, next_y)
            keep_going = True

    return beam_count

def solve_puzzle_part2():
    # Read the input
    # manifold_layout = SAMPLE_INPUT.split('\n')
    manifold_layout = read_lines(__file__)

    manifold_layout = tuple([tuple(x) for x in manifold_layout])

    beam_count = _project_beam(TachyonBeam(len(manifold_layout[0])//2, 0), 
                               manifold_layout)
    print(f"Beam count {beam_count}")


if __name__ == "__main__":
    solve_puzzle_part2()