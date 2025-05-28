import sys
from dfs import depth_first_search
from bfs import breadth_first_search
from ucs import uniform_cost_search

from gbfs import greedy_best_first_search
from a_star import a_star_search


class Maze:

    def __init__(self, filename):

        # Read file and set height and width of maze
        with open(filename) as f:
            contents = f.read()

        # Validate start and end goal
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one goal")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        # Determine the height and width of maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Keep track of walls
        self.walls = []  # Binary map that specifies if a cell is a wall or not.

        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    match contents[i][j]:
                        case "A":
                            self.start = (i, j)
                            row.append(False)
                        case "B":
                            self.goal = (i, j)
                            row.append(False)
                        case " ":
                            row.append(False)
                        case _:
                            row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None  # A valid solution is of the form (actions, cells)

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()

        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("#", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1)),
        ]

        result = []
        for action, (r, c) in candidates:
            if (
                0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]
            ):  # Cell is not invalid(i.e. out of bounds) nor is it a wall
                result.append((action, (r, c)))
        return result

    def solve(self, algorithm):
        self.num_explored = 0
        match algorithm:
            case "dfs":
                return depth_first_search(self)
            case "bfs":
                return breadth_first_search(self)
            case "ucs":
                return uniform_cost_search(self)
            case "gbfs":
                return greedy_best_first_search(self)
            case "a_star":
                return a_star_search(self)

    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw

        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",  # mode
            (
                self.width * cell_size,
                self.height * cell_size,
            ),  # (width, height) in pixels
            "black",
        )

        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # Solution:
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)

                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    (
                        [
                            (
                                j * cell_size + cell_border,
                                i * cell_size + cell_border,
                            ),  # Top-left corner & we leave an outward border.
                            (
                                (j + 1) * cell_size - cell_border,
                                (i + 1) * cell_size - cell_border,
                            ),  # Bottom-right corner. We are calculating this set of coordinates using the next/
                        ]
                    ),  # Sequence of [(x0, y0), (x1, y1)]
                    fill=fill,
                )
        img.save(filename)


if len(sys.argv) != 3:
    sys.exit(
        "Usage: python main.py maze.txt <algorithm.py> \n e.g. python main.py maze1.txt dfs.py>"
    )

m = Maze(sys.argv[1])
algorithm_file = sys.argv[2][:-3]
print("Maze:")
m.print()
print("Solving...")
m.solve(algorithm_file)
print("State Explored: ", m.num_explored)
print("Solution: ")
m.print()
m.output_image("maze.png", show_explored=True)
