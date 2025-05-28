import math
import heapq
from typing import Optional
from dfs import StackFrontier

cost_for_action = {
    "up": 2,
    "down": 2,
    "left": 5,
    "right": 5,
}


class Node:
    def __init__(self, state, parent, action, cost, heuristic=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.heuristic = heuristic

    def __lt__(self, other):
        return self.cost + self.heuristic < self.cost + other.heuristic


class PriorityQueue(StackFrontier):
    def add(self, node: Node) -> None:
        heapq.heappush(self.frontier, node)

    def remove(self) -> Optional[Node]:
        if self.empty():
            raise Exception("Can't remove from an empty frontier")
        return heapq.heappop(self.frontier)


# Manhattan distance (default)
def manhattan_distance(maze, node: Node) -> int:
    return abs(node.state[0] - maze.goal[0]) + abs(node.state[1] - maze.goal[1])


# Cartesian (Euclidean) distance
def cartesian_distance(maze, node: Node) -> float:
    return math.sqrt(
        (node.state[0] - maze.goal[0]) ** 2 + (node.state[1] - maze.goal[1]) ** 2
    )


# Heuristic function selector (defaults to manhattan)
def heuristic_function(maze, node: Node, method=manhattan_distance):
    return method(maze, node)


def a_star_search(maze, method=cartesian_distance):
    """
    Greedy Best-First Search (GBFS) implementation.
    """

    # Keep track of the number of states explored
    maze.num_explored = 0

    # Initialize a frontier to just the starting point
    start = Node(state=maze.start, parent=None, action=None, cost=0)
    start.heuristic = heuristic_function(maze, start, method)
    frontier = PriorityQueue()
    frontier.add(start)

    # Initialize an empty explored set
    maze.explored = set()

    while not frontier.empty():
        # Pop the node with the smallest heuristic in the frontier i.e. closest to goal
        node = frontier.remove()
        maze.num_explored += 1

        # Goal test
        if node.state == maze.goal:
            actions = []
            cells = []

            while node.parent is not None:
                actions.append(node.action)
                cells.append(node.state)
                node = node.parent

            actions.reverse()
            cells.reverse()
            maze.solution = (actions, cells)
            return

        # Add node to explored set
        maze.explored.add(node.state)

        # Expand the node
        for action, state in maze.neighbors(node.state):
            if not frontier.contains_state(state) and state not in maze.explored:
                child = Node(
                    state=state,
                    parent=node,
                    action=action,
                    cost=node.cost + cost_for_action[action],
                )
                child.heuristic = heuristic_function(maze, child, method)
                frontier.add(child)
