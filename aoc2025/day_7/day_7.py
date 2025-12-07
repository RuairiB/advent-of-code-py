"""
Advent of Code 2025 - Day 7

https://adventofcode.com/2025/day/7

See instructions.md for problem description.
"""

import json
from collections import defaultdict

from pretty_print_tree import animate_beams, create_animation_frames, print_tree, reconstruct_dfs_path
from requests_cache import CachedSession

# stole this from Kevin
INPUT = (
    CachedSession()
    .get(
        "https://adventofcode.com/2025/day/7/input",
        cookies=json.load(open("cookie.json")),
    )
    .content.strip()
    .decode()
    .splitlines()
)

EXAMPLE_INPUT = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............""".splitlines()  # noqa: W291


def solution(
    raw_input: list[str] = EXAMPLE_INPUT,
    final_visual: bool = False,
    progress_visual: bool = False,
) -> int:
    start = raw_input[0].index("S")

    beams: list[defaultdict[int, int]] = [defaultdict(lambda: 0) for _ in range(len(raw_input))]
    beams[0][start] = 1
    splits = set()

    for ridx, rstr in enumerate(raw_input[1:]):
        for pos, amount in beams[ridx].items():
            if raw_input[ridx + 1][pos] == ".":
                beams[ridx + 1][pos] = beams[ridx + 1][pos] + amount
            elif raw_input[ridx + 1][pos] == "^":
                beams[ridx + 1][pos - 1] = beams[ridx + 1][pos - 1] + amount
                beams[ridx + 1][pos + 1] = beams[ridx + 1][pos + 1] + amount
                splits.add((pos, ridx + 1))
            else:
                raise ValueError(f"Found something I didn't expect in pos {pos} of row {ridx + 1} of the tree:\n{rstr}")

    # 99% of my time was spent on getting the parsing right for pictures
    if final_visual:
        print_tree(raw_input, beam_pos=beams[1:])
    if progress_visual:
        dfs_path = reconstruct_dfs_path(beams[1:])
        beam_frames = create_animation_frames(dfs_path=dfs_path, final_changes=beams[1:])
        animate_beams(raw_input, beam_frames)

    print(f"Part 1:\t{len(splits)}")
    print(f"Part 2:\t{sum(beams[-1].values())}")


if __name__ == "__main__":
    # set progress_visual=True for animations, but it's fairly large for the actual solution
    print("----- Example Input -----")
    solution(EXAMPLE_INPUT, final_visual=True, progress_visual=False)

    print("----- Solution -----")
    solution(INPUT, final_visual=True, progress_visual=False)
