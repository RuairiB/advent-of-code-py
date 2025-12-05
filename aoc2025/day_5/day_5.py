"""
Advent of Code 2025 - Day 5

https://adventofcode.com/2025/day/5

See instructions.md for problem description.
"""

import itertools
import json

from requests_cache import CachedSession

# stole this from Kevin's repo
INPUT = (
    CachedSession()
    .get(
        "https://adventofcode.com/2025/day/5/input",
        cookies=json.load(open("cookie.json")),
    )
    .content.strip()
    .decode()
    .splitlines()
)

EXAMPLE_INPUT = """3-5
10-14
16-20
12-18

1
5
8
11
17
32
""".splitlines()


def part_1(input: list[str] = INPUT) -> int:
    split_input = [list(y) for x, y in itertools.groupby(input, lambda z: z == "") if not x]

    fresh_ranges = [tuple(map(int, line.split("-"))) for line in split_input[0]]
    test_ids = [int(line) for line in split_input[1]]

    valid_ids = set()
    for test_id in test_ids:
        for start, end in fresh_ranges:
            if start <= test_id <= end:
                valid_ids.add(test_id)
                break

    return len(valid_ids)


def part_2(input: list[str] = INPUT) -> int:
    split_input = [list(y) for x, y in itertools.groupby(input, lambda z: z == "") if not x]

    fresh_ranges = [tuple(map(int, line.split("-"))) for line in split_input[0]]

    valid_ids_count = 0
    fresh_ranges.sort()
    merged_ranges = []
    current_start, current_end = fresh_ranges[0]
    for start, end in fresh_ranges[1:]:
        if start <= current_end + 1:
            current_end = max(current_end, end)
        else:
            merged_ranges.append((current_start, current_end))
            current_start, current_end = start, end

    merged_ranges.append((current_start, current_end))

    # just need the length of each merged range
    for start, end in merged_ranges:
        valid_ids_count += end - start + 1

    return valid_ids_count


if __name__ == "__main__":
    print("Part 1 (example):", part_1(EXAMPLE_INPUT))
    print("Part 1:", part_1(INPUT))

    print("Part 2 (example):", part_2(EXAMPLE_INPUT))
    print("Part 2:", part_2(INPUT))
