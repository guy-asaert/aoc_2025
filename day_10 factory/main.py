from dataclasses import dataclass
import sys
import re
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils import read_lines

SAMPLE_INPUT = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""

MACHINE_REGEX = r"\[(?P<light_diagram>[.#]+)\]\s+" + \
                r"(?P<wiring_schematics>(?:\([0-9, ]+\)\s+)+)" + \
                r"(?P<jotage_requirements>\{[0-9, ]+\})"

@dataclass
class Machine:
    light_diagram: list[bool]
    wiring_schematics: list[int]
    other_wiring_schematics: list[tuple[int]]
    joltage_requirements: list[int]


def solve_puzzle_part1():
    # Read the input

    machines = []
    # for line in SAMPLE_INPUT.split('\n'):
    for line in read_lines(__file__):
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
        machines.append(Machine(light_diagram, wiring_schematics, 
                                other_wiring_schematics, joltage_requirements))

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

    # Sort out the joltage
    total_presses = 0
    for machine in machines:
        button_count = len(machine.joltage_requirements)
        start_joltage = button_count * [0]

        joltage_states = set()
        joltage_states.add(tuple(start_joltage))

        go_on_go_on = True
 
        button_presses = 0
        while go_on_go_on:
            next_joltage_states = set()
            button_presses += 1
            print(f"Searching for machine with joltage requirements {machine.joltage_requirements} in {button_presses} presses, "
                  f"currently have {len(joltage_states)} states to search")
            while joltage_states and go_on_go_on:
                joltage_state = joltage_states.pop()
                for schematic in machine.other_wiring_schematics:
                    next_joltage_state = list(joltage_state[:])
                    mask = 1
                    for i in schematic:
                        next_joltage_state[i] += 1
                        if next_joltage_state[i] > machine.joltage_requirements[i]:
                            next_joltage_state.clear()
                            break
                    if next_joltage_state == machine.joltage_requirements:
                        print(f"Found a solution for machine with joltage requirements "
                              f"{machine.joltage_requirements} in {button_presses} presses!")
                        go_on_go_on = False
                        total_presses += button_presses
                        break
                    if next_joltage_state:
                        next_joltage_states.add(tuple(next_joltage_state))
            if not next_joltage_states:
                raise ValueError(f"No more states to search for machine with joltage "
                                 f"requirements {machine.joltage_requirements}, giving up")
            joltage_states = next_joltage_states
    
    print(f"Total presses to get to the joltage levels: {total_presses}")                





if __name__ == "__main__":
    solve_puzzle_part1()