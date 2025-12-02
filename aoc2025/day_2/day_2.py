"""
Advent Of Code 2025 - Day 2

https://adventofcode.com/2025/day/2

See instructions.md for problem description.
"""

from pathlib import Path


def read_input(input_file: Path | str) -> list[int]:
    nums = []
    with Path(input_file).open("r") as f:
        for line in f:
            ranges = [r.split("-") for r in line.split(",")]
            for pair in ranges:
                nums.extend(range(int(pair[0]), int(pair[1]) + 1))

    return nums


def is_invalid_id_1(id: int | str) -> bool:
    """Check if an ID is invalid (part 1).

    Invalid IDs:
    - made *only* of some sequence of digits repeated twice (55, 6464, 123123, 222222)
    """
    if isinstance(id, int):
        id = str(id)

    if len(id) % 2 != 0:
        return False

    halfway = int(len(id) / 2)
    return id[:halfway] == id[halfway:]


def part_1(inputs: list[int]) -> int:
    # brute force
    return sum([int(id) for id in inputs if is_invalid_id_1(id)])


def is_invalid_id_2(id: int | str) -> bool:
    """Check if an ID is invalid (part 2).

    Invalid IDs:
    - made only of some sequence of digits repeated at least twice.
      e.g. 12341234 (1234 two times),
           123123123 (123 three times),
           1212121212 (12 five times),
           1111111 (1 seven times)

    An alternative, faster and more elegant solution (from https://stackoverflow.com/a/29489919)
    ```
    i = (id + id).find(id, 1, -1)
    return False if i == -1 else True
    ```

    Using regex would also be a lot faster than what's below:
    "(.+?)\1+$" will match the repeated substring _only_ if it's the only thing in the string.

    The solution here is my best non-regex attempt (since the regex took me ages to figure out)
    """
    if isinstance(id, int):
        id = str(id)

    len_id = len(id)
    # largest substring is half the string
    for i in range(1, len(id) // 2 + 1):
        if len_id % i:
            continue
        s = id[0:i]  # test substring
        if s * (len_id // i) == id:
            return True

    return False


def part_2(inputs: list[int]) -> int:
    # brute force
    return sum([int(id) for id in inputs if is_invalid_id_2(id)])


if __name__ == "__main__":
    print("Advent Of Code Day 2")
    example_input_ranges = read_input(Path(__file__).parent / "example_input.txt")
    input_ranges = read_input(Path(__file__).parent / "input.txt")

    print("Part 1 (example input):")
    print(part_1(example_input_ranges))

    print("Part 1 (real input):")
    print(part_1(input_ranges))

    print("\nPart 2 (example input):")
    print(part_2(example_input_ranges))

    print("Part 2 (real input):")
    print(part_2(input_ranges))
