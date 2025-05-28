from dfs import Node, StackFrontier


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("can't remove from an empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


def breadth_first_search(maze):
    """
    Finds  a solution to maze using breadth first search algorithm, if one exists.
    This algorithm employs a queue, which is a FIFO(Fast In, First Out) data structure.
    """
    # Keep track of number of states explored
    maze.num_explored = 0

    # Initialize frontier to just the starting position
    start = Node(state=maze.start, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(start)

    # Initialize an empty explored set
    maze.explored = set()

    # Keep looping until solution is found
    while True:
        # if nothing is in the frontier, then no path
        if frontier.empty():
            raise Exception("no path found")

        # Choose a node from the frontier
        node = frontier.remove()
        maze.num_explored += 1

        # Goal test: if the node is the goal, then we have a solution
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

        # Mark the node as explored
        maze.explored.add(node.state)

        # Expand its neighbors by adding them to the frontier
        for action, state in maze.neighbors(node.state):
            if not frontier.contains_state(state) and state not in maze.explored:
                child = Node(state=state, parent=node, action=action)
                frontier.add(child)
