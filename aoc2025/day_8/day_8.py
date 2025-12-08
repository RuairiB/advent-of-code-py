"""
Advent of Code 2025 - Day 8

https://adventofcode.com/2025/day/8

See instructions.md for problem description.
"""

import json
import math

from requests_cache import CachedSession

# stole this from Kevin
INPUT = (
    CachedSession()
    .get(
        "https://adventofcode.com/2025/day/8/input",
        cookies=json.load(open("cookie.json")),
    )
    .content.strip()
    .decode()
    .splitlines()
)

EXAMPLE_INPUT = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689""".splitlines()  # noqa: W291


def euclid_dist(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2) ** 0.5


def solution(
    raw_input: list[str] = EXAMPLE_INPUT,
    n_connections: int = 10,
    n_largest: int = 3,
) -> int:
    points: list[tuple[int, int, int]] = [tuple(map(int, line.split(","))) for line in raw_input]

    distances: dict[tuple[int, int], float] = {}
    for i, point_a in enumerate(points):
        for j, point_b in enumerate(points):
            if i < j:
                distances[(i, j)] = euclid_dist(point_a, point_b)

    distances_sorted = sorted(distances.items(), key=lambda x: x[1])

    # "union-find" / "disjoint set" to track components
    parent = list(range(len(points)))
    num_components = len(points)

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])  # Path compression
        return parent[x]

    part1_result = None
    part2_result = None

    for idx, ((i, j), _) in enumerate(distances_sorted):
        root_i, root_j = find(i), find(j)

        if root_i != root_j:
            parent[root_i] = root_j
            num_components -= 1

            # Part 1: n_connections edges
            if idx + 1 == n_connections:
                component_sizes: dict[int, int] = {}
                for node in range(len(points)):
                    root = find(node)
                    component_sizes[root] = component_sizes.get(root, 0) + 1
                part1_result = math.prod(sorted(component_sizes.values(), reverse=True)[:n_largest])

            # Part 2: all points connected (assuming it's after n_connections)
            if num_components == 1:
                part2_result = points[i][0] * points[j][0]
                break

    print(f"Part 1:\t{part1_result}")
    print(f"Part 2:\t{part2_result}")
    return part1_result, part2_result


if __name__ == "__main__":
    print("----- Example Input -----")
    solution(EXAMPLE_INPUT, n_connections=10)

    print("----- Solution -----")
    solution(INPUT, n_connections=1000)
