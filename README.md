# 2D_path: Problem Statement
Determine whether a path exists between two points that only crosses black pixels. 
Define a path as a sequence of pixels such that each pixel in the path is adjacent to the next pixel in the path

### Approach
We can solve this by treating the image as a grid graph of black “walkable” pixels and then running a breadth first search (BFS) 
to find disjoint paths between the requested endpoints. 

### Step by Step Approach

1. Load the PNG universe into a NumPy array and convert it to a 2D boolean array walkable where, 
   True means a black pixel that we are allowed to step on.

2. A path is a sequence of adjacent pixels: i.e from (x, y) we can step to (x +- 1, y) or (x, y +- 1)

3. Run BFS from the start pixel to the end pixel restricted to walkable cells (black), 
   keeping predecessors so that we can reconstruct a path if it exists.

4. For two disjoint paths, we:
   a. Find a path for the first pair.
   b. Temporarily mark those pixels as non walkable and search for the second pair.
   c. If that fails, try the opposite order (second pair then first).
   d. Only accept the result if the two paths share no pixels.

### Set Up Project - How to Run?
Note: All the commands are for macOS/Linux

1. Create a python virtual environment
```bash
python3 -m venv .venv
```

2. Activate the virtual environment
```bash
source venv/bin/activate
```

3. Install requirements
```bash
pip install -r requirements.txt
```
