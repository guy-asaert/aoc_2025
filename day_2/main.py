import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils import read_lines
from collections import namedtuple

SAMPLE_INPUT = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124"""

IDRange = namedtuple("IDRange", ["from_id", "to_id"])

def part1():
    # Read the input
    line = read_lines(__file__)[0]
    # line = SAMPLE_INPUT

    part_one_invalid_ids = 0
    part_two_invalid_ids = 0
    id_ranges = line.split(',')
    for id_range in id_ranges:
        lower, upper = id_range.split('-')
        id_range = IDRange(int(lower), int(upper))
        for i in range(id_range.from_id, id_range.to_id + 1):
            # print(i)
            id_string = str(i)
            string_length = len(id_string)
            # find all ways the string can be devided into equal parts

            for n in range(1, string_length // 2 + 1):
                if string_length % n == 0:  # dividable by n
                    sub_ids = set()
                    from_pos = 0
                    to_pos = n
                    while from_pos < string_length:
                        sub_ids.add(id_string[from_pos: to_pos])
                        if len(sub_ids) > 1:
                            break
                        from_pos += n
                        to_pos += n

                    if len(sub_ids) == 1:
                        part_two_invalid_ids += i
                        # print(id_string)
                        if string_length % 2 == 0 and n == string_length // 2:
                            part_one_invalid_ids += i
                            print(f'Part 1 {id_string}')
                        # Remove the following line for part one. Need it for
                        # part two.
                        break


    print(f"Added invalid ids is {part_one_invalid_ids}")
    print(f"Added invalid ids is {part_two_invalid_ids}")

if __name__ == "__main__":
    part1()
