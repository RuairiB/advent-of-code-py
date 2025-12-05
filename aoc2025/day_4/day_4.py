"""
Advent of Code 2025 - Day 4

https://adventofcode.com/2025/day/4

See instructions.md for problem description.
"""

from pathlib import Path


def read_input(input_file: Path | str) -> list[list[int]]:
    paper_roll_grid = []
    with Path(input_file).open("r") as f:
        for line in f:
            paper_roll_grid.append([1 if char == "@" else 0 for char in line.strip()])
    return paper_roll_grid


def part_1(paper_roll_grid: list[list[int]], debug: bool = False) -> int:
    """Count number of sites in grid that have fewer than 4 adjacent rolls/"@"s in the 8 adjacent cells.

    Optionally print out the grid with valid sites marked with "x" for debugging."""
    rows = len(paper_roll_grid)
    cols = len(paper_roll_grid[0]) if rows > 0 else 0
    paper_roll_grid_print = [row.copy() for row in paper_roll_grid]

    def count_adjacent(r: int, c: int) -> int:
        adjacent_positions = [
            (r - 1, c - 1),
            (r - 1, c),
            (r - 1, c + 1),
            (r, c - 1),
            (r, c + 1),
            (r + 1, c - 1),
            (r + 1, c),
            (r + 1, c + 1),
        ]

        count = 0
        for rr, cc in adjacent_positions:
            if 0 <= rr < rows and 0 <= cc < cols:
                count += paper_roll_grid[rr][cc]
        return count

    valid_sites = 0
    for r in range(rows):
        for c in range(cols):
            if paper_roll_grid_print[r][c] == 1 and count_adjacent(r, c) < 4:
                valid_sites += 1
                if debug:
                    paper_roll_grid_print[r][c] = "x"

    if debug:
        for row in paper_roll_grid_print:
            row = ["@" if cell == 1 else "." if cell == 0 else cell for cell in row]
            print("".join(str(cell) for cell in row))

    return valid_sites


def part_2(paper_roll_grid: list[list[int]], debug: bool = False) -> int:
    """Now, after identifying the removable rolls, remove them (i.e. replace 1 with 0),
    and repeat until no more can be removed.

    Return the total number of rolls removed.

    Why reuse code when you can duplicate it?"""
    rows = len(paper_roll_grid)
    cols = len(paper_roll_grid[0]) if rows > 0 else 0
    total_removed = 0
    while True:
        removed_this_round = 0
        paper_roll_grid_print = [row.copy() for row in paper_roll_grid]

        def count_adjacent(r: int, c: int) -> int:
            adjacent_positions = [
                (r - 1, c - 1),
                (r - 1, c),
                (r - 1, c + 1),
                (r, c - 1),
                (r, c + 1),
                (r + 1, c - 1),
                (r + 1, c),
                (r + 1, c + 1),
            ]

            count = 0
            for rr, cc in adjacent_positions:
                if 0 <= rr < rows and 0 <= cc < cols:
                    count += paper_roll_grid[rr][cc]
            return count

        for r in range(rows):
            for c in range(cols):
                if paper_roll_grid[r][c] == 1 and count_adjacent(r, c) < 4:
                    paper_roll_grid[r][c] = 0
                    paper_roll_grid_print[r][c] = "x"
                    removed_this_round += 1

        if debug:
            for row in paper_roll_grid_print:
                row = ["@" if cell == 1 else "." if cell == 0 else cell for cell in row]
                print("".join(str(cell) for cell in row))
            print()

        total_removed += removed_this_round
        if removed_this_round == 0:
            break

    return total_removed


if __name__ == "__main__":
    example_input_file = Path(__file__).parent / "example_input.txt"
    example_paper_roll_grid = read_input(example_input_file)
    example_result_part_1 = part_1(example_paper_roll_grid, debug=True)
    print(f"Example Part 1: Number of valid sites = {example_result_part_1}")

    input_file = Path(__file__).parent / "input.txt"
    paper_roll_grid = read_input(input_file)
    result_part_1 = part_1(paper_roll_grid)
    print(f"Part 1: Number of valid sites = {result_part_1}")

    example_result_part_2 = part_2(example_paper_roll_grid, debug=True)
    print(f"Example Part 2: Total rolls removed = {example_result_part_2}")
    result_part_2 = part_2(paper_roll_grid)
    print(f"Part 2: Total rolls removed = {result_part_2}")
