"""
Advent of Code 2025 - Day 10

https://adventofcode.com/2025/day/10

See instructions.md for problem description.
"""

import json

import numpy as np
from requests_cache import CachedSession
from scipy.optimize import linprog

# stole this from Kevin
INPUT = (
    CachedSession()
    .get(
        "https://adventofcode.com/2025/day/10/input",
        cookies=json.load(open("cookie.json")),
    )
    .content.strip()
    .decode()
    .splitlines()
)

EXAMPLE_INPUT = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}""".splitlines()  # noqa: W291


def parse_input(raw_input: list[str]) -> list[tuple[list[bool], list[set[int]], list[int]]]:
    parsed = []
    for line in raw_input:
        lights_part, *button_parts, joltage_part = line.split(" ")
        lights: list[bool] = [c == "#" for c in lights_part.strip("[]")]
        buttons = [set(map(int, part.strip("()").split(","))) for part in button_parts]
        joltage_reqs = list(map(int, joltage_part.strip("{}").split(",")))
        parsed.append((lights, buttons, joltage_reqs))
    return parsed


def solution(raw_input: list[str] = EXAMPLE_INPUT, debug_flag: bool = False) -> tuple[int, int]:
    parsed_input = parse_input(raw_input)
    total_presses_lights = 0
    total_presses_joltage = 0

    for machine_index, (lights, buttons, joltage_reqs) in enumerate(parsed_input):
        n = len(lights)
        m = len(buttons)
        min_presses_lights = float("inf")
        min_presses_joltage = float("inf")

        # part 1: brute force lol - check all 2^m(?) combinations. should use xor's instead
        min_presses_lights = float("inf")
        for press_mask in range(1 << m):
            current_lights = [False] * n
            presses = 0

            for button_index in range(m):
                if (press_mask >> button_index) & 1:
                    presses += 1
                    for light_index in buttons[button_index]:
                        current_lights[light_index] = not current_lights[light_index]

            if current_lights == lights:
                min_presses_lights = min(min_presses_lights, presses)

        # part 2: LP:
        # minimise sum(presses) where sum(presses[i] * button_effects[i][j]) >= joltage_reqs[j] for all j
        # in matrices: Ax >= b, minimise c^T x, where A is button effects, b is joltage_reqs, c is all 1s
        # Z3 would be the easy way to do this, but I'll use scipy first (which is just as easy...):
        # gaussian elim should be used to optimise things, but I'm not arsed
        def solve_machine(joltage_reqs: list[int], buttons: list[set[int]], debug: bool = False) -> int:
            c = np.ones(m, dtype=int)
            A = np.zeros((n, m), dtype=int)  # button effects
            b = np.array(joltage_reqs, dtype=int)  # required joltage

            for button_index, button in enumerate(buttons):
                for joltage_index in button:
                    A[joltage_index][button_index] = 1

            if debug:
                print(f"Machine {machine_index} optimization setup:")
                print(f"c: {c}")
                print(f"A (button effects): {A}")
                print(f"b (joltage reqs): {b}")

            res = linprog(
                c,
                A_eq=A,
                b_eq=b,
                bounds=(0, None),
                # the most important line. spend a solid hour confused why it wasn't working without it:
                integrality=np.ones(m, dtype=int),
                method="highs",
            )
            if debug:
                print(f"x: {res.x}")

            if res.success:
                return int(sum(np.round(res.x)))  # shouldn't need rounding with proper integrality
            else:
                return float("inf")

        min_presses_joltage = solve_machine(joltage_reqs, buttons, debug=debug_flag)
        if debug_flag:
            print(f"Machine {machine_index} Min presses (lights): {min_presses_lights}")
            print(f"Machine {machine_index} Min presses (joltage): {min_presses_joltage}")

        total_presses_lights += min_presses_lights
        total_presses_joltage += min_presses_joltage

    print(f"Part 1: {total_presses_lights}")
    print(f"Part 2: {total_presses_joltage}")
    return total_presses_lights, total_presses_joltage


if __name__ == "__main__":
    print("----- Example Input -----")
    solution(EXAMPLE_INPUT, debug_flag=True)

    print("----- Solution -----")
    solution(INPUT, debug_flag=False)
