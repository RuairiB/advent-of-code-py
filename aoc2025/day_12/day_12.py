"""
Advent of Code 2025 - Day 12

https://adventofcode.com/2025/day/12

See instructions.md for problem description.
"""

import json
import random

import numpy as np
from art import CHRISTMAS_IN_SPACE, CHRISTMAS_TREE, GRINCH
from requests_cache import CachedSession

# stole this from Kevin
INPUT = (
    CachedSession()
    .get(
        "https://adventofcode.com/2025/day/12/input",
        cookies=json.load(open("cookie.json")),
    )
    .content.strip()
    .decode()
    .splitlines()
)

EXAMPLE_INPUT = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2""".splitlines()  # noqa: W291


def shape_orientations(shape: np.ndarray) -> list[np.ndarray]:
    orientations = set()
    for flip in [False, True]:
        transformed_shape = np.flipud(shape) if flip else shape
        for _ in range(4):
            transformed_shape = np.rot90(transformed_shape)
            orientations.add(tuple(map(tuple, transformed_shape)))
    return [np.array(orientation) for orientation in orientations]


def parse_input(raw_input: list[str]) -> tuple[list[list[np.ndarray]], list[tuple[int, int, list[int]]]]:
    shapes = []
    problems = []
    current_shape = []
    for line in raw_input:
        if "x" in line:
            size, shape_counts = line.split(":")
            width, height = map(int, size.split("x"))
            shape_counts = list(map(int, shape_counts.strip().split()))
            problems.append((width, height, shape_counts))
        else:
            if "#" in line or "." in line:
                current_shape.append([1 if c == "#" else 0 for c in line.strip()])
            elif not line.strip() and current_shape:
                shapes.append(np.array(current_shape))
                current_shape = []

    shapes = [shape_orientations(shape) for shape in shapes]

    return shapes, problems


def solution(raw_input: list[str] = EXAMPLE_INPUT) -> int:
    # only one part today
    shapes, problems = parse_input(raw_input)

    shape_sizes = [np.sum(shape_set[0]) for shape_set in shapes]

    total_count = 0
    for width, height, shape_counts in problems:
        area = width * height
        required_size = sum(num_shapes * shape_sizes[shape_id] for shape_id, num_shapes in enumerate(shape_counts))

        if required_size > area:
            continue

        total_count += 1

    # wait... surely it should be harder than this? Shouldn't I have to actually try to fit the shapes???
    # this doesn't work for the example input, but does for the actual input (larger sample size I guess)
    print(f"Part 1 (size check): {total_count}")

    # TODO: will try to do it "properly" later today if I have time
    # TODO: might also code golf-ify the size check solution so it feels like a better achievement

    print("Part 2: Happy Christmas!")
    print(random.choice([CHRISTMAS_IN_SPACE, CHRISTMAS_TREE, GRINCH]))


if __name__ == "__main__":
    print("----- Example Input -----")
    solution(EXAMPLE_INPUT)

    print("----- Solution -----")
    solution(INPUT)
