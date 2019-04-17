import time
import math 
import numpy as np

def decision(grid):
    tic = time.clock()
    depth = 4
    a = -np.inf
    b = np.inf
    return maximize(grid,a,b, depth)

def maximize(grid, a, b, tic, depth):
    if check_gameover(grid) or depth == 0 or (time.clock()-tic) > 0.02:
        print "Time limit exceeded"
        return evaluate(grid)
    max_utility = -np.inf 
    children = []
    for move in grid.get AvailableMoves():
        child = get_child(grid, move)
        children.append(child)
    for child in grid.children():
        utility = minimize(child, a, b, tic, depth-1)
        if utility > max_utility:
            max_utility = utililty
        if max_utlity >= beta:
            break
        a = max(max_utility, a)
    return max_utility

def minimize(grid, a,b, tic, depth):

    if check_gameover(grid) or depth == 0 or (time.clock()-tic) > 0.02:
        print "Time limit exceeded"
        return Eval(grid)
    min_utility = np.inf 
    empty_cells = grid.getAvailableCells();

    children = []
    for cell in empty_cells:
        grid2_copy = grid.clone()
        grid4_copy = grid.clone()
        grid2_copy.insertTile(cell, 2)
        grid4_copy.insertTile(cell, 4)
        children.append(grid2_copy)
        children.append(grid4_copy)

    #Children- random tile possibilities for grid state 
    #calc. utility for every child 
    for child in children:
        utility = maximize(child,a,b,tic, depth-1)
        if utility < min_utility:
            min_utility = utility 
        if min_utililty <= a:
            break
        b = min(min_utility, b) 
    return min_utility

#-------------------------------------------------------------------------

def get_child(grid, dir):
     dir = int(dir)
     grid_copy = grid.clone()
     grid_copy.move(dir)
     return grid_copy

def check_gameover(grid):
     return not grid.canMove()

def evaluate(grid):

