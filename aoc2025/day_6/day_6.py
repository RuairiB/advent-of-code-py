"""
Advent of Code 2025 - Day 6

https://adventofcode.com/2025/day/6

See instructions.md for problem description.
"""

import json
import math

from requests_cache import CachedSession

# stole this from Kevin
INPUT = (
    CachedSession()
    .get(
        "https://adventofcode.com/2025/day/6/input",
        cookies=json.load(open("cookie.json")),
    )
    .content.strip()
    .decode()
    .splitlines()
)

EXAMPLE_INPUT = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
""".splitlines()  # noqa: W291


def parse_rows(raw_input: list[str]) -> list[list[str]]:
    """
    transpose & split appropriately:
    [
      "123 328  51 64 ",
      " 45 64  387 23 ",
      "  6 98  215 314",
      "*   +   *   +  "
    ]
    -> [
      ["123", " 45", "  6", "*  "],
      ["328", "64 ", "98 ", "+  "],
      [" 51", "387", "215", "*  "],
      ["64 ", "23 ", "314", "+  "],
    ]
    """
    col_width: list[int] = list(
        map(int, list(map(max, map(list, zip(*[map(len, r.split()) for r in raw_input[:-1]])))))
    )
    n = len(raw_input[0].split())

    new_cols = [["" for _ in range(len(raw_input))] for _ in range(n)]
    pos = 0
    for c in range(n):
        for r in range(len(raw_input)):
            new_cols[c][r] = raw_input[r][pos : pos + col_width[c]]
        pos += col_width[c] + 1

    return new_cols


def solution(raw_input: list[str] = EXAMPLE_INPUT) -> None:
    rot_input: list[list[str]] = parse_rows(raw_input)
    total_1 = 0
    total_2 = 0

    def parse_num_pt_2(nums: list[str]) -> list[int]:
        """
        ["64 ", "23 ", "314"] -> [4, 431, 623]
        """
        n = max(map(len, nums))
        new_nums = []
        for idx in reversed(range(n)):
            new_num = ""
            for num in nums:
                new_num += num[idx]

            new_nums.append(new_num)
        return list(map(int, new_nums))

    for col in rot_input:
        op: str = col[-1]
        if op.strip() == "*":
            total_1 += math.prod(map(int, col[:-1]))
            total_2 += math.prod(parse_num_pt_2(col[:-1]))
        elif op.strip() == "+":
            total_1 += sum(map(int, col[:-1]))
            total_2 += sum(parse_num_pt_2(col[:-1]))

    print(f"Part 1:    {total_1}")
    print(f"Part 2:    {total_2}")


if __name__ == "__main__":
    print("----- Example Input -----")
    solution(EXAMPLE_INPUT)

    print("----- Solution -----")
    solution(INPUT)
