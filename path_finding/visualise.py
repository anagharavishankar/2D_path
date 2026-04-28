from typing import List, Tuple

import imageio.v3 as imageio
import numpy as np

Coord = Tuple[int, int]


def ensure_rgb(img: np.ndarray) -> np.ndarray:
    """
    Ensure the image is 3 channel uint8 RGB for easy coloring.
    """
    if img.ndim == 2:
        img_rgb = np.stack([img] * 3, axis=2)
    elif img.ndim == 3 and img.shape[2] == 3:
        img_rgb = img
    else:
        raise ValueError("Unsupported image shape for visualization")
    return img_rgb.astype(np.uint8)


def draw_path(
        img: np.ndarray,
        path: List[Coord],
        color: Tuple[int, int, int] = (255, 0, 0),
) -> np.ndarray:
    """
    return a copy of img with the path drawn on top in the given RGB color.
    """
    out = ensure_rgb(img.copy())
    for x, y in path:
        if 0 <= y < out.shape[0] and 0 <= x < out.shape[1]:
            out[y, x] = color
    return out


def draw_two_paths(
        img: np.ndarray,
        path1: List[Coord],
        path2: List[Coord],
        color1: Tuple[int, int, int] = (0, 0, 255),
        color2: Tuple[int, int, int] = (255, 0, 0),
) -> np.ndarray:
    """
    draw two non intersecting paths in two different colors.
    """
    out = ensure_rgb(img.copy())
    for x, y in path1:
        if 0 <= y < out.shape[0] and 0 <= x < out.shape[1]:
            out[y, x] = color1
    for x, y in path2:
        if 0 <= y < out.shape[0] and 0 <= x < out.shape[1]:
            out[y, x] = color2
    return out


def save_path_visualization(
        in_path: str,
        out_path: str,
        path: List[Coord],
        color: Tuple[int, int, int] = (255, 0, 0),
) -> None:
    """
    load image from in_path, draw path, save to out_path.
    """
    img = imageio.imread(in_path)
    img_out = draw_path(img, path, color)
    imageio.imwrite(out_path, img_out)


def save_two_paths_visualization(
        in_path: str,
        out_path: str,
        path1: List[Coord],
        path2: List[Coord],
) -> None:
    """
    load image, draw two paths, and save.
    """
    img = imageio.imread(in_path)
    img_out = draw_two_paths(img, path1, path2)
    imageio.imwrite(out_path, img_out)
