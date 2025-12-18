import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils import read_lines
from collections import namedtuple

SAMPLE_INPUT = """987654321111111
811111111111119
234234234234278
818181911112111"""


def highest_joltage(bank, num_cells):
    if len(bank) < num_cells:
        return None
    
    sorted_bank = sorted(set(bank), reverse=True)

    keep_looking = True
    highest_index = 0
    next_highest = ''

    num_cells -= 1
    print(f"Number of cells left: {num_cells}")
    while keep_looking:
        keep_looking = False
        highest_location = bank.index(sorted_bank[highest_index])
        highest_battery_joltage = sorted_bank[highest_index]
        print(f"Trying batterty with joltage of {highest_battery_joltage}")
        if num_cells > 0:
            if highest_location + num_cells >= len(bank):
                print("Not enough batteries left to get a full set")
                keep_looking = True
            else:
                next_highest = highest_joltage(bank[highest_location + 1:], num_cells)
                if not next_highest:
                    keep_looking = True
                else:
                    break

            highest_index += 1
            if highest_index >= len(sorted_bank):
                return None
                # raise RuntimeError("Cannot solve puzzle")

    return bank[highest_location] + next_highest
    

def part1():
    # Read the input
    banks = read_lines(__file__)
    # banks = SAMPLE_INPUT.split()

    sum_of_joltage = 0
    for bank in banks:
        print(bank)
        sorted_by_joltage = sorted(bank, reverse=True)
        print(sorted_by_joltage)
        index_high = bank.index(sorted_by_joltage[0])
        index_low = bank.index(sorted_by_joltage[1])
        if index_high <= index_low: # the normal/easy case
            print(bank[index_high] + bank[index_low])
            sum_of_joltage += int(bank[index_high] + bank[index_low])
        elif index_high == len(bank) - 1:
            print(bank[index_low] + bank[index_high])
            sum_of_joltage += int(bank[index_low] + bank[index_high])
        else:
            look_here = bank[index_high + 1:]
            sorted_for_low = sorted(look_here, reverse=True)
            print(bank[index_high] + sorted_for_low[0])
            sum_of_joltage += int(bank[index_high] + sorted_for_low[0])

    print(f'Total joltage is {sum_of_joltage}')

def part1_v2(batteries: int = 2):
    # Read the input
    banks = read_lines(__file__)
    # banks = SAMPLE_INPUT.split()

    sum_of_joltage = 0
    for bank in banks:
        highest_joltage_in_bank = highest_joltage(bank, batteries)
        print(highest_joltage_in_bank)
        sum_of_joltage += (int(highest_joltage_in_bank))

    print(f'Total joltage V2 is {sum_of_joltage}')



if __name__ == "__main__":
    # part1()
    # part1_v2()
    part1_v2(12)
