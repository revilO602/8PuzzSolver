from heapq import *
from Node import Node
import numpy as np


class Solver:
    def __init__(self, goal_state, rows_am, cols_am):
        self.goal_state = goal_state
        self.rows_am = rows_am
        self.cols_am = cols_am
        self.goal_coord = {}

    # Creates a dictionary of numbers in the goal state and their coordinates
    # to be used by the second heuristic function
    def set_goal_cord(self):
        for y, row in enumerate(self.goal_state):
            for x, num in enumerate(row):
                if num != 0:
                    self.goal_coord[num] = (y, x)

    # First heuristic function, returns number of misplaced numbers
    def get_hvalue1(self, node_state):
        hvalue = 0
        for i, row in enumerate(node_state):
            for j, num in enumerate(row):
                if num != 0 and num != self.goal_state[i][j]:
                    hvalue += 1
        return hvalue

    # Second heuristic function, returns the sum of distances of number positions from their goal positions.
    def get_hvalue2(self, node_state):
        hvalue = 0
        for i, row_node in enumerate(node_state):
            for j, num in enumerate(row_node):
                if num != 0:
                    hvalue += abs(i - self.goal_coord[num][0]) + abs(j - self.goal_coord[num][1])
        return hvalue

    def a_star(self, start_node, h_function):
        heap = []
        generated_count = 0
        opened_count = 0
        max_depth = 0
        generated_states = {start_node.state.copy().tostring()}
        heappush(heap, (start_node.value, generated_count, start_node))
        while not np.array_equal(heap[0][2].state, self.goal_state):
            opened_count += 1
            new_children = heappop(heap)[2].make_children(self.rows_am, self.cols_am)
            for child in new_children:
                if child.state.copy().tostring() not in generated_states:
                    generated_states.add(child.state.copy().tostring())
                    child.value = h_function(child.state) + child.depth
                    generated_count += 1
                    max_depth = max(max_depth, child.depth)
                    heappush(heap, (child.value, generated_count, child))
        print(' '.join(["Hlbka", str(max_depth), "Generated nodes =",
                        str(generated_count), "Opened nodes =", str(opened_count)]))
        return heappop(heap)[2]

    def solve(self, start_state, h_function=3):
        if h_function == 1:
            hf = self.get_hvalue1
        else:
            self.set_goal_cord()
            if h_function == 2:
                hf = self.get_hvalue2
            else:
                hf = lambda state: self.get_hvalue1(state) + self.get_hvalue2(state)
        first_node = Node(start_state, None, None)
        first_node.value = hf(first_node.state) + first_node.depth
        print(first_node.value)
        last_node = self.a_star(first_node, hf)
        path = []
        while last_node is not None:
            path.append((last_node.state, last_node.op))
            last_node = last_node.parent
        return path
