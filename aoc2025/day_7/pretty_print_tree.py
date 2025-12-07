import sys
from collections import defaultdict

from asciimatics.effects import Print
from asciimatics.exceptions import StopApplication
from asciimatics.renderers import StaticRenderer
from asciimatics.scene import Scene
from asciimatics.screen import Screen

# needed for DFS on the actual input. Clearly it's all massively inefficient...
sys.setrecursionlimit(10000)


def print_tree(base: list[str], beam_pos: list[defaultdict[int, int]] | None = None):
    print_str = base
    if beam_pos:
        if len(beam_pos) == len(base):
            print_str = create_beam_str(base, beam_pos[1:])
        else:
            print_str = create_beam_str(base, beam_pos)

    for r in print_str:
        print(r)


def create_beam_str(base: list[str], beam_pos: list[defaultdict[int, int]]) -> list[str]:
    print_str = base.copy()
    for bidx, bpos in enumerate(beam_pos):
        for pos in bpos:
            if print_str[bidx + 1][pos] == ".":
                print_str[bidx + 1] = print_str[bidx + 1][:pos] + "|" + print_str[bidx + 1][pos + 1 :]
            elif print_str[bidx + 1][pos] == "^":
                print("There's a mistake somewhere, found '^' where the beam is supposed to go:")
                print(f"bidx ({bidx}), pos ({pos}): {print_str[bidx + 1]}")
                raise ValueError("bad strings, see debug above")

    return print_str


def reconstruct_dfs_path(final_changes: list[dict[int, int]]) -> list[tuple[int, int]]:
    # should have just done this for the actual solution...
    R = len(final_changes)

    max_c = 0
    for row_dict in final_changes:
        if row_dict:
            max_c = max(max_c, max(row_dict.keys()))
    C = max_c + 1

    visited = [[False for _ in range(C)] for _ in range(R)]
    dfs_path = []

    DIRECTIONS = [
        (-1, -1),
        (1, -1),
        (-1, 0),
        (1, 0),
        (0, -1),
        (-1, 1),
        (1, 1),
        (0, 1),
    ]

    def dfs(r, c):
        if not (0 <= r < R and 0 <= c < C):
            return

        if visited[r][c]:
            return

        if c not in final_changes[r]:
            return

        visited[r][c] = True
        dfs_path.append((r, c))

        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            dfs(nr, nc)

    dfs(0, list(final_changes[0].keys())[0])

    return dfs_path


def create_animation_frames(
    dfs_path: list[tuple[int, int]], final_changes: list[dict[int, int]]
) -> list[list[dict[int, int]]]:
    R = len(final_changes)
    current_changes = [{} for _ in range(R)]
    animation_frames = []

    for r, c in dfs_path:
        change_flag = final_changes[r][c]

        current_changes[r][c] = change_flag

        frame_state = [d.copy() for d in current_changes]
        animation_frames.append(frame_state)

    return animation_frames


def animate_frames(screen: Screen, frames: list[str]):
    renderers = [StaticRenderer([f]) for f in frames]

    all_lines = []
    for frame_string in frames:
        all_lines.extend(frame_string.split("\n"))

    WIDTH = max([len(line) for line in all_lines if line]) if all_lines else 0
    HEIGHT = max([len(f.split("\n")) for f in frames])

    scenes = []

    for renderer in renderers:
        effect = Print(
            screen,
            renderer,
            y=(screen.height - HEIGHT) // 2,
            x=(screen.width - WIDTH) // 2,
            speed=0,
            colour=Screen.COLOUR_WHITE,
        )

        scenes.append(Scene([effect], duration=5, clear=False))

    try:
        screen.clear()
        screen.play(scenes, repeat=False)
    except StopApplication:
        pass
    except Exception as e:
        print(f"Animation error: {e}")
        raise


def animate_beams(base: list[str], beam_frames: list[list[defaultdict[int, int]]]):
    frames = ["\n".join(create_beam_str(base, beam)) for beam in beam_frames]
    Screen.wrapper(animate_frames, arguments=[frames])
