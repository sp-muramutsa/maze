class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("can't remove from an empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


def depth_first_search(maze):
    """
    Finds  a solution to maze using depth first search algorithm, if one exists.
    This algorithm employs a stack, which is a LIFO(Last In, First Out) data structure.
    """

    # Keep track of the number of states explored
    maze.num_explored = 0

    # Initialize a frontier to just the starting point
    start = Node(state=maze.start, parent=None, action=None)
    frontier = StackFrontier()
    frontier.add(start)

    # Initialize an empty explored set
    maze.explored = set()

    # Keep looping until the solution is found
    while True:
        if frontier.empty():
            raise Exception("no solution")

        # Choose a node to expand
        node = frontier.remove()
        maze.num_explored += 1

        # Goal test
        if node.state == maze.goal:  # Backtrack to collect the solution
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

        # Mark node as explored
        maze.explored.add(node.state)

        # Add neighbors to frontier
        for action, state in maze.neighbors(node.state):
            if not frontier.contains_state(state) and state not in maze.explored:
                child = Node(state=state, parent=node, action=action)
                frontier.add(child)
