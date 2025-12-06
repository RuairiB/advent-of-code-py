"""
Advent Of Code 2025 - Day 3

https://adventofcode.com/2025/day/3

See instructions.md for problem description.
"""

from pathlib import Path


def read_input(input_file: Path | str) -> list[int]:
    battery_banks = []
    with Path(input_file).open("r") as f:
        for line in f:
            battery_banks.append([int(x) for x in line.strip()])
    return battery_banks


def part_1(inputs: list[list[int]]) -> int:
    max_joltage = 0
    for row in inputs:
        # joltage = max 2 digit number from row without reordering digits
        joltage = max(row[i] * 10 + row[j] for i in range(len(row)) for j in range(len(row)) if i < j)
        max_joltage += joltage

    return max_joltage


def calculate_max_joltage_brute_force(row: list[int]) -> int:
    # This will be correct, but is incredibly stupid and won't ever finish, it's just here for reference
    joltage = max(
        row[i] * 10**11
        + row[j] * 10**10
        + row[k] * 10**9
        + row[l] * 10**8
        + row[m] * 10**7
        + row[n] * 10**6
        + row[o] * 10**5
        + row[p] * 10**4
        + row[q] * 10**3
        + row[r] * 10**2
        + row[s] * 10**1
        + row[t] * 10**0
        for i in range(len(row))
        for j in range(len(row))
        for k in range(len(row))
        for l in range(len(row))
        for m in range(len(row))
        for n in range(len(row))
        for o in range(len(row))
        for p in range(len(row))
        for q in range(len(row))
        for r in range(len(row))
        for s in range(len(row))
        for t in range(len(row))
        if i < j < k < l < m < n < o < p < q < r < s < t
    )
    return joltage


def calculate_max_joltage(row: list[int], length: int) -> str:
    # should have read it in as strings to begin with
    row_str = "".join(str(x) for x in row)
    if length == 0:
        return ""
    next_digit: str = str(max(row_str[: len(row_str) - length + 1]))
    next_digit_pos: int = row_str.find(next_digit)
    return next_digit + calculate_max_joltage(row_str[next_digit_pos + 1 :], length - 1)


def part_2(inputs: list[list[int]]) -> int:
    max_joltage = 0
    for row in inputs:
        joltage = calculate_max_joltage(row, length=12)
        max_joltage += int(joltage)
    return max_joltage


if __name__ == "__main__":
    example_data = read_input(Path(__file__).parent / "example_input.txt")
    input_data = read_input(Path(__file__).parent / "input.txt")

    print("Part 1: (example)", part_1(example_data))
    print("Part 1: (input)", part_1(input_data))

    print("Part 2: (example)", part_2(example_data))
    print("Part 2: (input)", part_2(input_data))
