"""
Advent of Code 2025 - Day 11

https://adventofcode.com/2025/day/11

See instructions.md for problem description.
"""

import json

from requests_cache import CachedSession

# stole this from Kevin
INPUT = (
    CachedSession()
    .get(
        "https://adventofcode.com/2025/day/11/input",
        cookies=json.load(open("cookie.json")),
    )
    .content.strip()
    .decode()
    .splitlines()
)

EXAMPLE_INPUT_PART_1 = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out""".splitlines()  # noqa: W291

EXAMPLE_INPUT_PART_2 = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out""".splitlines()  # noqa: W291


def count_paths_dag(
    graph: dict[str, list[str]],
    start: str,
    end: str,
    cache: dict[str, int] | None = None,
) -> int:
    # I think this will fail if the graph isn't a dag/has cycles? tbh I'm still crap with graphs
    if cache is None:
        cache = {}

    if start == end:
        return 1

    if start in cache:
        return cache[start]

    total = 0
    for neighbor in graph.get(start, []):
        total += count_paths_dag(graph, neighbor, end, cache)

    cache[start] = total
    return total


def count_paths_with_visits(
    graph: dict[str, list[str]],
    start: str,
    end: str,
    required: set[str],
    cache: dict[tuple[str, frozenset[str]], int] | None = None,
) -> int:
    if cache is None:
        cache = {}

    def dfs(node: str, visited_required: frozenset[str]) -> int:
        # dfs with memoization & tracking visited required nodes
        if node in required:
            visited_required = visited_required | {node}

        if node == end:
            return 1 if visited_required == required else 0

        if (node, visited_required) in cache:
            return cache[(node, visited_required)]

        total = 0
        for neighbor in graph.get(node, []):
            total += dfs(neighbor, visited_required)

        cache[(node, visited_required)] = total
        return total

    return dfs(start, frozenset())


def solution(raw_input: dict[int, list[str]]) -> None:
    graph_1: dict[str, list[str]] = {(parts := line.split(": "))[0]: parts[1].split() for line in raw_input[1]}
    graph_2: dict[str, list[str]] = {(parts := line.split(": "))[0]: parts[1].split() for line in raw_input[2]}

    print(f"Part 1: {count_paths_dag(graph_1, 'you', 'out')}")
    # num_paths from 'svr' to 'out', which also visit 'fft' and 'dac' at least once
    print(f"Part 2: {count_paths_with_visits(graph_2, start='svr', end='out', required={'fft', 'dac'})}")


if __name__ == "__main__":
    print("----- Example Input -----")
    solution({1: EXAMPLE_INPUT_PART_1, 2: EXAMPLE_INPUT_PART_2})

    print("----- Solution -----")
    solution({1: INPUT, 2: INPUT})
