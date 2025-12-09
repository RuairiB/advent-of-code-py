"""
Advent of Code 2025 - Day 9

https://adventofcode.com/2025/day/9

See instructions.md for problem description.
"""

import itertools
import json

from requests_cache import CachedSession

# stole this from Kevin
INPUT = (
    CachedSession()
    .get(
        "https://adventofcode.com/2025/day/9/input",
        cookies=json.load(open("cookie.json")),
    )
    .content.strip()
    .decode()
    .splitlines()
)

EXAMPLE_INPUT = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3""".splitlines()  # noqa: W291


def area(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(a[0] - b[0] + 1) * abs(a[1] - b[1] + 1)


def solution(raw_input: list[str] = EXAMPLE_INPUT) -> int:
    corners = [tuple(map(int, line.split(","))) for line in raw_input]

    print(f"Part 1: {max([area(*c) for c in itertools.combinations(corners, 2)])}")

    def green_lines(line: list[tuple[tuple[int, int], tuple[int, int]]]) -> list[tuple[int, int, int, int]]:
        return [(min(a, c), min(b, d), max(a, c), max(b, d)) for (a, b), (c, d) in line]

    # precompute valid _lines_
    valid_lines = green_lines(itertools.pairwise(corners + [corners[0]]))
    max_area = 0

    for x, y, u, v in green_lines(itertools.combinations(corners, 2)):
        size = (u - x + 1) * (v - y + 1)

        if size > max_area:
            for p, q, r, s in valid_lines:
                if x < r and y < s and u > p and v > q:
                    break

            else:
                max_area = max(max_area, size)

    print(f"Part 2: {max_area}")


if __name__ == "__main__":
    print("----- Example Input -----")
    solution(EXAMPLE_INPUT)

    print("----- Solution -----")
    solution(INPUT)
