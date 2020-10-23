from Solver import Solver
from timeit import default_timer as timer
import numpy as np

def load_input():
    m, n = input("Zadajte velkost m x n\n").split(" ", 1)
    m = int(m)
    n = int(n)
    start_state = np.arange(m*n).reshape(m, n)
    goal_state = np.arange(m*n).reshape(m, n)
    for i in range(0, int(m)):
        for j, num in enumerate(input().split(" ")):
            start_state[i, j] = int(num)
    for i in range(0, int(m)):
        for j, num in enumerate(input().split(" ")):
            goal_state[i, j] = int(num)
    return m, n, start_state, goal_state


def translate_operator(op):
    if op == 'r':
        return 'LEFT'
    elif op == 'l':
        return 'RIGHT'
    elif op == 'u':
        return 'DOWN'
    elif op == 'd':
        return 'UP'


def output_path(path):
    path.reverse()
    for step in path:
        if step[1] is not None:
            print(translate_operator(step[1]))
        else:
            print("START")
        for row in step[0]:
            print(' '.join(str(i) for i in row))
        print('\n')


rows_am, cols_am, start_state, goal_state = load_input()
solver = Solver(goal_state, rows_am, cols_am)

start = timer()
path = solver.solve(start_state, 1)
end = timer()
print(end - start)
output_path(path)

start = timer()
path = solver.solve(start_state, 2)
end = timer()
print(end - start)
output_path(path)

start = timer()
path = solver.solve(start_state, 3)
end = timer()
print(end - start)
output_path(path)
