from dataclasses import dataclass
import sys
import re
from pathlib import Path
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
sys.path.append(str(Path(__file__).parent.parent))

from line_profiler import LineProfiler
from utils import read_lines

SAMPLE_INPUT = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""

MACHINE_REGEX = r"\[(?P<light_diagram>[.#]+)\]\s+" + \
                r"(?P<wiring_schematics>(?:\([0-9, ]+\)\s+)+)" + \
                r"(?P<jotage_requirements>\{[0-9, ]+\})"

@dataclass
class Machine:
    index: int
    light_diagram: list[bool]
    wiring_schematics: list[int]
    other_wiring_schematics: list[tuple[int]]
    joltage_requirements: list[int]


def solve_puzzle_part1(machines):
    # Sort out the lights
    total_presses = 0
    for machine in machines:
        go_on_go_on = True
        all_states = set()
        search_states = set()
        search_states.add(machine.light_diagram)
        presses = 0
        while go_on_go_on:
            next_search_states = set()
            presses += 1
            for schematic in machine.wiring_schematics:
                for search_state in search_states:
                    next_light_state = search_state ^ schematic
                    if next_light_state in all_states: # already seen this state, skip it
                        continue
                    all_states.add(next_light_state)
                    if next_light_state == 0:
                        print(f"Found a solution in {presses} presses!")
                        go_on_go_on = False
                        break
                    next_search_states.add(next_light_state)
            if not next_search_states:
                print("No more states to search, giving up")
                go_on_go_on = False
            search_states = next_search_states
        
        print(f"Found a solution for machine with light diagram {machine.light_diagram} in {presses} presses")
        total_presses += presses

    print(f"Total presses: {total_presses}")


machines = []

def match_joltage(machine_index):
    """Find the minimum button presses to match joltage requirements using MILP."""
    machine = machines[machine_index]
    n_buttons = len(machine.other_wiring_schematics)
    n_wires = len(machine.joltage_requirements)

    # A[i, j] = 1 if wire i is incremented by button j
    A = np.zeros((n_wires, n_buttons), dtype=float)
    for j, schematic in enumerate(machine.other_wiring_schematics):
        for i in schematic:
            A[i, j] = 1.0

    b = np.array(machine.joltage_requirements, dtype=float)
    c = np.ones(n_buttons, dtype=float)  # minimise total presses

    constraints = LinearConstraint(A, lb=b, ub=b)  # A @ x = b exactly
    bounds = Bounds(lb=0)                           # x_j >= 0
    integrality = np.ones(n_buttons)               # all integer

    result = milp(c, constraints=constraints, integrality=integrality, bounds=bounds)
    if result.success:
        return int(round(result.fun))
    return -1  # no solution

def solve_puzzle_part2(machines, profiler=None):
    """ Solve the second part of the puzzle """
    total_presses = 0
    for i in range(len(machines)):
        min_presses = match_joltage(i)
        print(f"Machine {i}: {min_presses} presses")
        total_presses += min_presses

    print(f"Total presses to get to the joltage levels: {total_presses}")                


if __name__ == "__main__":
    
    # for index, line in enumerate(SAMPLE_INPUT.split('\n')):
    for index, line in enumerate(read_lines(__file__)):
        match = re.match(MACHINE_REGEX, line)
        if not match:
            raise ValueError(f"Line {line} does not match the expected format")
        light_diagram_binary = ['1' if c == '#' else '0' for c in match.group('light_diagram')]
        light_diagram = int("".join(reversed(light_diagram_binary)), 2)
        wiring_schematics = []
        other_wiring_schematics = []
        for wiring_schematic in re.findall(r"\([0-9, ]+\)", match.group('wiring_schematics')):
            wires = tuple(int(i) for i in wiring_schematic[1:-1].split(','))
            wire_int = 0
            for wire in wires:
                wire_int += (1 << wire)
            wiring_schematics.append(wire_int)
            other_wiring_schematics.append(wires)   
        joltage_requirements = [int(i) for i in match.group('jotage_requirements')[1:-1].split(',')]
        machines.append(Machine(index, light_diagram, wiring_schematics, 
                                other_wiring_schematics, joltage_requirements))
    # solve_puzzle_part1(machines)
    solve_puzzle_part2(machines)

    # profiler = LineProfiler()
    # profiler_wrapper = profiler(solve_puzzle_part2)
    # try:
    #     profiler_wrapper(machines, profiler=profiler)
    # except KeyboardInterrupt:
    #     print("\nInterrupted — printing partial profiler results:")
    # finally:
    #     profiler.print_stats()
