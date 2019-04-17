from random import randint
from BaseAI import BaseAI
import numpy as np
import time
import math 

class PlayerAI(BaseAI):
    def __init__(self):
        pass

    def getMove(self,grid):
        max_utility = -np.inf
        direction = None
        for move in grid.getAvailableMoves():
            child = self.get_child(grid, move)
            utility = self.decision(child, max=False)
            if utility >= max_utility:
                max_utility = utility
                direction = move 
        return direction

    def decision(self, grid, max=True):
        tic = time.clock()
        depth = 4
        a = -np.inf
        b = np.inf
        if max:
            return self.maximize(grid,a,b,tic,depth)
        else:
            return self.minimize(grid,a,b,tic,depth)


    def maximize(self, grid, a, b, tic, depth):
        if self.check_gameover(grid) or depth == 0 or (time.clock()-tic) > 0.02:
            #print depth
            return self.evaluate(grid)
        max_utility = -np.inf 
        children = []
        for move in grid.getAvailableMoves():
            child = self.get_child(grid, move)
            children.append(child)
        for child in children:
            utility = self.minimize(child, a, b, tic, depth-1)
            if utility > max_utility:
                max_utility = utility
            if max_utility >= b:
                break
            a = max(max_utility, a)
        return max_utility

    def minimize(self,grid,a,b,tic, depth):

        if self.check_gameover(grid) or depth == 0 or (time.clock()-tic) > 0.02:
            #print depth 
            return self.evaluate(grid)
        min_utility = np.inf 
        empty_cells = grid.getAvailableCells()

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
            utility = self.maximize(child,a,b,tic, depth-1)
            if utility < min_utility:
                min_utility = utility 
            if min_utility <= a:
                break
            b = min(min_utility, b) 
        return min_utility

    #-------------------------------------------------------------------------

    def get_child(self,grid,dir):
         dir = int(dir)
         grid_copy = grid.clone()
         grid_copy.move(dir)
         return grid_copy

    def check_gameover(self,grid):
         return not grid.canMove()

    def evaluate(self,grid):
        grid_copy = grid.clone()
        cells = grid.getAvailableCells()
        moves = grid.getAvailableMoves()
        max_value = self.get_max_tile(grid_copy)
        smoothness = self.smoothness(grid_copy)
        s = 1.0/(2**(int(smoothness/100.0)))
        mono = (self.monoticity(grid_copy))
        grad = self.grad(grid_copy)
        total= (s)+(6*mono)+(3*len(cells))+(6*grad)
        #total = (2.7*len(cells))+(2*len(moves))+(2*grad)
        
        return total

    def get_max_tile(self,grid):
        grid = grid.map	
        max_value = max(max(grid, key=lambda x: max(x)))
        if grid[0][0] or grid[0][3] or grid[3][0] or grid[3][3] == max_value:
        #if grid[0][0] == max_value:
            return 10e2
        else:
            return -10e2

    def smoothness(self, grid):
        size = grid.size
        grid = grid.map
        s = 0
        for row in grid:
            for c in range(size-1):
                s += abs(row[c] - row[c + 1])
                pass
        for j in range(size):
            for k in range(size - 1):
                s += abs(grid[k][j] - grid[k + 1][j])
        return s

    def monoticity(self,grid):
        size = grid.size
        g_map = grid.map
        mono = 0
        for row in g_map:
            diff = row[0] - row[1]
            for i in range(size - 1):
                if (row[i] - row[i + 1]) * diff <= 0:
                    mono += 1
                diff = row[i] - row[i + 1]

        for j in range(size):
            diff = g_map[0][j] - g_map[1][j]
            for k in range(size - 1):
                if (g_map[k][j] - g_map[k + 1][j]) * diff <= 0:
                    mono += 1
                diff = g_map[k][j] - g_map[k + 1][j]

        return mono

     
    def grad(self, grid):
        g_map = grid.map
        g = [
            [[ 3,  2,  1,  0],[ 2,  1,  0, -1],[ 1,  0, -1, -2],[ 0, -1, -2, -3]],
            [[ 0,  1,  2,  3],[-1,  0,  1,  2],[-2, -1,  0,  1],[-3, -2, -1, -0]], 
            [[ 0, -1, -2, -3],[ 1,  0, -1, -2],[ 2,  1,  0, -1],[ 3,  2,  1,  0]], 
            [[-3, -2, -1,  0],[-2, -1,  0,  1],[-1,  0,  1,  2],[ 0,  1,  2,  3]]]
        values = [0]*4 
        for i in range(4):
            for r in range(4):
                for c in range(4):
                    values[i] += g[i][r][c]*g_map[r][c]
        return max(values)









 

