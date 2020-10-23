# One node in the graph of states
class Node:
    def __init__(self, state, parent, op):
        self.state = state  # Puzzle state - represents arrangement of the puzzle for this node
        self.parent = parent  # Parent Node
        self.op = op  # Operator used on parent node to get to this node - l|r|u|d = LEFT|RIGHT|UP|DOWN
        if parent is None:
            self.depth = 0
        else:
            self.depth = parent.depth + 1
        self.value = None  # Value used by the priority queue

    def __lt__(self, other):
        return self.value <= other.value

    # Locate the empty spot in the puzzle, in this stage of the program its the movable spot
    def find_mover(self):
        for y, row in enumerate(self.state):
            for x, pos in enumerate(row):
                if pos == 0:
                    return y, x
        print("Couldnt find mover")

    # Returns new state after applying operator to current state
    def get_new_state(self, mover_x, mover_y, op):
        new_state = self.state.copy()
        if op == 'r':
            new_state[mover_y, mover_x] = new_state[mover_y, mover_x + 1]
            new_state[mover_y, mover_x + 1] = 0
        elif op == 'l':
            new_state[mover_y, mover_x] = new_state[mover_y, mover_x - 1]
            new_state[mover_y, mover_x - 1] = 0
        elif op == 'u':
            new_state[mover_y, mover_x] = new_state[mover_y - 1, mover_x]
            new_state[mover_y - 1, mover_x] = 0
        elif op == 'd':
            new_state[mover_y, mover_x] = new_state[mover_y + 1, mover_x]
            new_state[mover_y + 1, mover_x] = 0
        return new_state

    # Create all the possible children nodes with operators LEFT, RIGHT, UP, DOWN (moving the mover)
    # Excludes making the parent
    def make_children(self, rows_am, cols_am):
        children = []
        mover_y, mover_x = self.find_mover()
        if self.op != 'l' and mover_x < cols_am - 1:
            children.append(Node(self.get_new_state(mover_x, mover_y, "r"),
                                 self, 'r'))
        if self.op != 'r' and mover_x > 0:
            children.append(Node(self.get_new_state(mover_x, mover_y, "l"),
                                 self, 'l'))
        if self.op != 'u' and mover_y < rows_am - 1:
            children.append(Node(self.get_new_state(mover_x, mover_y, "d"),
                                 self, 'd'))
        if self.op != 'd' and mover_y > 0:
            children.append(Node(self.get_new_state(mover_x, mover_y, "u"),
                                 self, 'u'))
        return children
