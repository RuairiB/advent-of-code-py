"""
Advent Of Code 2025 - Day 1: Part 1

https://adventofcode.com/2025/day/1

See instructions.md for problem description.
"""

from pathlib import Path


class Dial:
    """
    Baby's first Python class for safecracking
    """

    def __init__(self, initial_value: int = 50) -> None:
        self._value = self._normalize(initial_value)

    @staticmethod
    def _normalize(value: int) -> int:
        return value % 100

    @property
    def value(self) -> int:
        return self._value

    def get_zero_crossing_count_for_increment(self, increment: int) -> int:
        """
        Count the number of zero crossings for a signed increment,
        does not increment value.
        """
        if not isinstance(increment, int):
            raise TypeError("increment must be an integer.")

        start_value = self._value
        new_value = start_value + increment  # w/o norm

        if new_value == 0:
            return 1

        # right
        if increment > 0:
            return new_value // 100

        # left
        abs_amount = abs(increment)
        if abs_amount <= start_value:
            return 0

        # start from zero, and turn left
        if start_value == 0:
            return (abs_amount - start_value) // 100

        # +1 crossing for reaching zero
        return 1 + ((abs_amount - start_value) // 100)

    def __add__(self, other: int):
        if not isinstance(other, int):
            return NotImplemented
        new_val = self._normalize(self._value + other)
        return Dial(new_val)

    def __sub__(self, other: int):
        if not isinstance(other, int):
            return NotImplemented
        new_val = self._normalize(self._value - other)
        return Dial(new_val)

    def __iadd__(self, other: int):
        if not isinstance(other, int):
            raise TypeError("Unsupported type for +=")
        self._value = self._normalize(self._value + other)
        return self

    def __isub__(self, other: int):
        if not isinstance(other, int):
            raise TypeError("Unsupported type for -=")
        self._value = self._normalize(self._value - other)
        return self

    def __repr__(self):
        return f"Dial({self._value})"

    def __str__(self):
        return f"Dial position: {self._value}"


def read_input(turns_file: Path | str) -> list[int]:
    turns = []
    with Path(turns_file).open("r") as f:
        for line in f:
            turn_abs_val = int(line[1:])
            if line[0] == "R":
                turns.append(turn_abs_val)
            elif line[0] == "L":
                turns.append(-1 * turn_abs_val)
            else:
                raise ValueError(f"Don't know what to do with this line: {line}")

    return turns


def part_1(turns: list[int]) -> None:
    safe_dial = Dial(initial_value=50)
    zero_count = 0
    for turn_val in turns:
        safe_dial += turn_val
        if safe_dial.value == 0:
            zero_count += 1

    print(f"Final dial value: {safe_dial}")
    print(f"Password: {zero_count}")


def part_2(turns: list[int]) -> None:
    safe_dial = Dial(initial_value=50)
    zero_count = 0
    for turn_val in turns:
        zero_count += safe_dial.get_zero_crossing_count_for_increment(turn_val)
        safe_dial += turn_val

    print(f"Final dial value: {safe_dial}")
    print(f"Password: {zero_count}")


if __name__ == "__main__":
    print("Advent Of Code Day 1")
    example_turns = read_input(Path(__file__).parent / "example_input.txt")
    input_turns = read_input(Path(__file__).parent / "input.txt")

    print("Part 1 (example input):")
    part_1(turns=example_turns)
    print("\nPart 1 (actual input):")
    part_1(turns=input_turns)

    print("\nPart 2 Password method 0x434C49434B (example input):")
    part_2(turns=example_turns)
    print("\nPart 2 Password method 0x434C49434B (actual input):")
    part_2(turns=input_turns)
