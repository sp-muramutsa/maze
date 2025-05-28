# AI Maze Solver

A Python project implementing multiple maze-solving algorithms to find and visualize paths through maze inputs.

## Features

- Supports various search algorithms:
  - Breadth-First Search (BFS)
  - Depth-First Search (DFS)
  - A* Search
  - Greedy Best-First Search (GBFS)
  - Uniform Cost Search (UCS)
- Reads maze layouts from text files.
- Visualizes the pathfinding process and final solution.
- Modular code structure with separate files for each algorithm.
- Easy to extend with additional algorithms or heuristics.

## Getting Started

## Requirements

- Python 3.x
- Required packages listed in `requirements.txt`

## Installation

```bash
pip install -r requirements.txt
```

## Usage
Run the main script with your maze input file:

```bash
python main.py maze1.txt
```
Replace maze1.txt with the desired maze file.

## Maze Format
The maze files are text-based grids.

Walls and paths are represented by specific characters (see example files).

## Search Algorithms
Each algorithm explores the maze differently:

## Uninformed Algorithms
- BFS guarantees the shortest path in an unweighted maze.

- DFS explores deeply but may not find the shortest path.

## Informed Algorithms (Artificially Intelligent)
- A* uses heuristics for efficient shortest path finding.

- GBFS uses heuristics to guide search but not always optimal.

- UCS finds the least costly path based on step costs.

## Author
CS50 & Sandrin Muramutsa
