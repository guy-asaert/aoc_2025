import sys
import math
from collections import Counter
from itertools import combinations
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils import read_lines
from collections import namedtuple
from functools import cache

JunctionBox = namedtuple("JunctionBox", "x y z")
DistanceDetails = namedtuple("DistanceDetails", "D FromJ ToJ ")

SAMPLE_INPUT = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""


def solve_puzzle_part1():
    # Read the input

    junction_boxes = []
    # for line in SAMPLE_INPUT.split('\n'):
    for line in read_lines(__file__):
        junction_boxes.append(JunctionBox(*(int(i) for i in line.split(','))))
    
    distances = []
    for junction_box_from, junction_box_to in combinations(junction_boxes, 2):
        distance_squared = \
            (junction_box_from.x - junction_box_to.x) ** 2 + \
            (junction_box_from.y - junction_box_to.y) ** 2 + \
            (junction_box_from.z - junction_box_to.z) ** 2
        distances.append(DistanceDetails(
            distance_squared, 
            junction_box_from, junction_box_to ))

    sorted_by_distance = sorted(distances, key = lambda x: x.D)

    circuits = dict()

    circuit_number = 1
    for distance_item in sorted_by_distance[:1000]:
        if distance_item.FromJ in circuits and distance_item.ToJ in circuits:
            # need to join two circuits
            unified_circuit_number = circuits[distance_item.FromJ]
            deleted_circuit_number = circuits[distance_item.ToJ]
            if unified_circuit_number != deleted_circuit_number:
                for circuit_item, circuit_id in circuits.items():
                    if circuit_id == deleted_circuit_number:
                        circuits[circuit_item] = unified_circuit_number
        elif distance_item.FromJ in circuits:
            circuits[distance_item.ToJ] = circuits[distance_item.FromJ]
        elif distance_item.ToJ in circuits:
            circuits[distance_item.FromJ] = circuits[distance_item.ToJ]
        else:
            circuits[distance_item.FromJ] = circuit_number
            circuits[distance_item.ToJ] = circuit_number
            circuit_number += 1

    counts = Counter(circuits.values())
    print(f"The answer is {math.prod([c for _, c in counts.most_common(3)])}")

def solve_puzzle_part2():
    # Read the input

    junction_boxes = []
    # for line in SAMPLE_INPUT.split('\n'):
    for line in read_lines(__file__):
        junction_boxes.append(JunctionBox(*(int(i) for i in line.split(','))))
    
    distances = []
    for junction_box_from, junction_box_to in combinations(junction_boxes, 2):
        distance_squared = \
            (junction_box_from.x - junction_box_to.x) ** 2 + \
            (junction_box_from.y - junction_box_to.y) ** 2 + \
            (junction_box_from.z - junction_box_to.z) ** 2
        distances.append(DistanceDetails(
            distance_squared, 
            junction_box_from, junction_box_to ))

    sorted_by_distance = sorted(distances, key = lambda x: x.D)

    circuits = dict()

    circuit_number = 1
    for distance_item in sorted_by_distance:
        if distance_item.FromJ in circuits and distance_item.ToJ in circuits:
            # need to join two circuits
            unified_circuit_number = circuits[distance_item.FromJ]
            deleted_circuit_number = circuits[distance_item.ToJ]
            if unified_circuit_number != deleted_circuit_number:
                for circuit_item, circuit_id in circuits.items():
                    if circuit_id == deleted_circuit_number:
                        circuits[circuit_item] = unified_circuit_number
        elif distance_item.FromJ in circuits:
            circuits[distance_item.ToJ] = circuits[distance_item.FromJ]
        elif distance_item.ToJ in circuits:
            circuits[distance_item.FromJ] = circuits[distance_item.ToJ]
        else:
            circuits[distance_item.FromJ] = circuit_number
            circuits[distance_item.ToJ] = circuit_number
            circuit_number += 1

        if len(circuits) == len(junction_boxes):
            counts = Counter(circuits.values())
            if len(counts) == 1:
                print(f"The answer for part 2 is {distance_item.FromJ.x * distance_item.ToJ.x}")
                break
                


if __name__ == "__main__":
    solve_puzzle_part2()