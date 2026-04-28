# main.py
import argparse

import imageio.v3 as imageio

from path_finding.core import (
    bfs_path,
    find_two_disjoint_paths,
    load_universe,
    path_exists,
)
from path_finding.visualise import (
    save_path_visualization,
    save_two_paths_visualization,
)


def parse_coord(text: str) -> tuple[int, int]:
    """
    Parse 'x,y' into (x, y).
    """
    x_str, y_str = text.split(",")
    return int(x_str), int(y_str)


def main() -> None:
    parser = argparse.ArgumentParser(description="2D black-pixel path finder")
    parser.add_argument("image", help="Input universe image (PNG)")
    parser.add_argument(
        "--start",
        type=parse_coord,
        help="Start coordinate 'x,y' for single path",
    )
    parser.add_argument(
        "--end",
        type=parse_coord,
        help="End coordinate 'x,y' for single path",
    )
    parser.add_argument(
        "--pair1",
        type=parse_coord,
        nargs=2,
        metavar=("S1", "E1"),
        help="Two coords 'x,y' 'x,y' for first pair",
    )
    parser.add_argument(
        "--pair2",
        type=parse_coord,
        nargs=2,
        metavar=("S2", "E2"),
        help="Two coords 'x,y' 'x,y' for second pair",
    )
    parser.add_argument(
        "--out",
        help="Optional output image path for visualization",
    )

    args = parser.parse_args()
    universe = load_universe(args.image)

    if args.start and args.end:
        sx, sy = args.start
        ex, ey = args.end
        exists = path_exists(universe, sx, sy, ex, ey)
        print(f"Path exists between {args.start} and {args.end}: {exists}")
        if exists and args.out:
            path = bfs_path(universe, (sx, sy), (ex, ey))
            assert path is not None
            save_path_visualization(args.image, args.out, path)
            print(f"Visualization saved to {args.out}")

    if args.pair1 and args.pair2:
        p1_start, p1_end = args.pair1
        p2_start, p2_end = args.pair2
        path1, path2 = find_two_disjoint_paths(
            universe, p1_start, p1_end, p2_start, p2_end
        )
        if path1 is None or path2 is None:
            print("Could not find two disjoint paths.")
        else:
            print("Found two disjoint paths.")
            if args.out:
                save_two_paths_visualization(args.image, args.out, path1, path2)
                print(f"Visualization with two paths saved to {args.out}")


if __name__ == "__main__":
    main()
