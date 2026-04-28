from collections import deque
from typing import Tuple, Optional, List

import imageio.v3 as imageio
import numpy as np

Coord = Tuple[int, int]


def load_universe(path: str, threshold: int = 128) -> np.ndarray:
    """
    Load an image and return a 2D boolean array where True means a black pixel
    (walkable) and False means white (blocked).
    """
    img = imageio.imread(path)

    # convert to grayscale [0, 255]
    if img.ndim == 3:
        # average over channels
        gray = img.mean(axis=2)
    else:
        gray = img.astype(np.float32)

    # black = intensity below threshold
    walkable = gray < threshold
    return walkable


def in_bounds(grid: np.ndarray, x: int, y: int) -> bool:
    h, w = grid.shape
    return 0 <= x < w and 0 <= y < h


def neighbors_4(x: int, y: int) -> List[Coord]:
    """ 4 connected neighborhood (up, down, left, right)"""
    return [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
    ]


def bfs_path(grid: np.ndarray, start: Coord, goal: Coord) -> Optional[List[Coord]]:
    """
   BFS on a boolean grid.

    grid[y, x] == True means the pixel is walkable (black).
    Returns a list of (x, y) from start to goal (inclusive) or None.
    """
    sx, sy = start
    gx, gy = goal

    if not in_bounds(grid, sx, sy) or not in_bounds(grid, gx, gy):
        return None
    if not grid[sy, sx] or not grid[gy, gx]:
        # start or goal not on a black pixel
        return None

    h, w = grid.shape
    visited = np.zeros((h, w), dtype=bool)
    prev: dict[Coord, Coord] = {}

    q: deque[Coord] = deque()
    q.append((sx, sy))
    visited[sy, sx] = True

    while q:
        x, y = q.popleft()
        if (x, y) == (gx, gy):
            # reconstruct path
            path: List[Coord] = []
            cur = (x, y)
            while cur in prev:
                path.append(cur)
                cur = prev[cur]
            path.append((sx, sy))
            path.reverse()
            return path

        for nx, ny in neighbors_4(x, y):
            if (
                    in_bounds(grid, nx, ny)
                    and grid[ny, nx]
                    and not visited[ny, nx]
            ):
                visited[ny, nx] = True
                prev[(nx, ny)] = (x, y)
                q.append((nx, ny))

    return None


def path_exists(universe: np.ndarray, start_x: int, start_y: int, end_x: int, end_y: int, ) -> bool:
    """
    universe: entire input
    API required by the task: return True if a black only path exists.
    """
    path = bfs_path(universe, (start_x, start_y), (end_x, end_y))
    return path is not None


def find_two_disjoint_paths(
        universe: np.ndarray,
        pair1_start: Coord,
        pair1_end: Coord,
        pair2_start: Coord,
        pair2_end: Coord,
) -> Tuple[Optional[List[Coord]], Optional[List[Coord]]]:
    """
    Try to find two black only paths that do not share pixels.

    Greedy strategy:
      1. Find a path for pair 1, then block it and find pair 2.
      2. If that fails, do the opposite order.
    """

    def attempt_order(
            first_start: Coord,
            first_end: Coord,
            second_start: Coord,
            second_end: Coord,
    ) -> Tuple[Optional[List[Coord]], Optional[List[Coord]]]:
        first_path = bfs_path(universe, first_start, first_end)
        if first_path is None:
            return None, None

        # block first path pixels
        blocked = universe.copy()
        for x, y in first_path:
            blocked[y, x] = False

        second_path = bfs_path(blocked, second_start, second_end)
        if second_path is None:
            return None, None

        return first_path, second_path

    # try pair1 then pair2
    p1, p2 = attempt_order(pair1_start, pair1_end, pair2_start, pair2_end)
    if p1 is not None and p2 is not None:
        # Double-check disjointness
        if set(p1).isdisjoint(p2):
            return p1, p2

    # try pair2 then pair1
    q2, q1 = attempt_order(pair2_start, pair2_end, pair1_start, pair1_end)
    if q1 is not None and q2 is not None and set(q1).isdisjoint(q2):
        # return to the original pair order
        return q1, q2
    return None, None
