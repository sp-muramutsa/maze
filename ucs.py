from dfs import StackFrontier
from typing import Optional, Tuple
import heapq

cost_for_action = {
    "up": 2,
    "down": 2,
    "left": 5,
    "right": 5,
}


class Node:
    def __init__(self, state, parent, action, cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost


class PriorityQueue(StackFrontier):
    def add(self, node: Node) -> None:
        heapq.heappush(self.frontier, node)

    def remove(self) -> Optional[Node]:
        if self.empty():
            raise Exception("can't remove from an empty frontier")
        else:
            node = heapq.heappop(self.frontier)
            return node

    def get_node(self, state: Tuple) -> Optional[Node]:
        for n in self.frontier:
            if n.state == state:
                return n

    def replace(self, node: Node) -> None:
        for i, n in enumerate(self.frontier):
            if n.state == node.state:
                self.frontier[i] = node
                heapq.heapify(self.frontier)
                break


def uniform_cost_search(maze):

    # Node with  initial state
    start = Node(state=maze.start, parent=None, action=None, cost=0)

    # Priority queue frontier ordered by PATH-COST with initial node as only element
    frontier = PriorityQueue()
    frontier.add(start)

    # Empty explored set
    maze.explored = set()

    # Keep track of the number of states explored
    maze.num_explored = 0

    # Keep looping till solution is found
    while True:
        # If the frontier is empty then return failure
        if frontier.empty():
            raise Exception("No solution")

        # Pop the lowest-cost node from the frontier
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

        # For each action in possible actions on this node state
        for action, state in maze.neighbors(node.state):
            child = Node(
                state=state,
                parent=node,
                action=action,
                cost=node.cost + cost_for_action[action],
            )
            # If a child is not in frontier or explored, add it to the frontier
            if not frontier.contains_state(state) and state not in maze.explored:
                frontier.add(child)

            # Elif the child is in the frontier with a higher path cost then replace the node with child
            elif frontier.contains_state(state):
                child_in_frontier = frontier.get_node(state)
                if child.cost < child_in_frontier.cost:
                    frontier.replace(child)
