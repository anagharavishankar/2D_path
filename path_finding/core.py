from collections import deque
from typing import List, Optional, Sequence, Tuple

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
