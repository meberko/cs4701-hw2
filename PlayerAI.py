from random import randint
from BaseAI import BaseAI
from copy import deepcopy

[TERM, MIN, MAX] = range(3)
moveIdx = [UP, DOWN, LEFT, RIGHT, RAND] = range(5)

fullBoard = []
for i in range(0,4):
    for j in range(0,4):
        fullBoard.append((i,j))

class Node:
    def __init__(self, children, minimax, metric, grid, move, depth):
        self.children = children
        self.minimax = minimax
        self.grid = grid
        self.metric = metric
        self.move = move
        self.depth = depth

    def __eq__(self, rhs):
        return self.grid == rhs.grid

class PlayerAI(BaseAI):
    def getMove(self, grid):
        moves = grid.getAvailableMoves()
        h = []
        tiledCells = self.getTiledCells(grid)
        minimaxTree = self.buildMinimaxTree(grid, 3)

        for move in moves:
            gridCopy = deepcopy(grid)
            gridCopy.move(move)
            h.append((move,self.getHeuristic(gridCopy)))
        print
        """print h
        print all(x[1] == h[0][1] for x in h)"""
        return sorted(h,key=lambda x: x[1], reverse=True)[0][0]
        #return moves[randint(0, len(moves) - 1)] if moves else None

    def getHeuristic(self, grid):
        # Copy grid
        gridCopy = deepcopy(grid)
        tiledCells = self.getTiledCells(gridCopy)
        totalCellValue = 0;

        # Get number of available cells
        nAvailableCells = len(gridCopy.getAvailableCells())
        for cell in tiledCells:
            totalCellValue += gridCopy.getCellValue(cell)
        h = totalCellValue*nAvailableCells/(16-nAvailableCells) + self.getNumAdjacent(gridCopy, tiledCells)
        return h

    def getNumAdjacent(self, grid, tiledCells):
        numAdj = 0
        for currCell in tiledCells:
            for i in range(1,len(tiledCells)):
                if grid.getCellValue(currCell)==grid.getCellValue(tiledCells[i]) and (currCell[0] - tiledCells[i][0])**2 + (currCell[1] - tiledCells[i][1])**2 == 1:
                    numAdj += 1
        return numAdj

    def getTiledCells(self, grid):
        return list(set(fullBoard) - set(grid.getAvailableCells()))

    def buildMinimaxTree(self, initGrid, depth):
        root = Node([], MAX, -1, initGrid, None, 0)
        queue = [root]
        currDepth = 0
        while depth - currDepth > 1:
            curr = queue.pop(0)
            if curr.depth == currDepth:
                if curr.minimax==MAX:
                    self.buildMaxChildren(curr)
                    print("Built %d Max children" % len(curr.children))
                if curr.minimax==MIN:
                    self.buildMinChildren(curr)
                    print("Built %d Min children" % len(curr.children))
                for child in curr.children:
                    queue.append(child)
            else:
                print "Increasing curr depth"
                currDepth += 1
                queue.insert(0,curr)
        while queue:
            curr = queue.pop(0)
            self.buildTermChildren(curr)
            print("Built %d Term children" % len(curr.children))
        return root

    def buildMaxChildren(self, currNode):
        children = []
        for move in currNode.grid.getAvailableMoves():
            gridCopy = deepcopy(currNode.grid)
            gridCopy.move(move)
            children.append(Node([], MIN, -1, gridCopy, move, currNode.depth + 1))
        currNode.children = children

    def buildMinChildren(self, currNode):
        children = []
        for availCell in currNode.grid.getAvailableCells():
            gridCopy = deepcopy(currNode.grid)
            gridCopy.insertTile(availCell, 2)
            children.append(Node([], MAX, -1, gridCopy, RAND, currNode.depth + 1))
        currNode.children = children

    def buildTermChildren(self, currNode):
        if currNode.minimax==MAX:
            children = []
            for move in currNode.grid.getAvailableMoves():
                gridCopy = deepcopy(currNode.grid)
                gridCopy.move(move)
                children.append(Node([], TERM, self.getHeuristic(gridCopy), gridCopy, move, currNode.depth + 1))
            currNode.children = children
        if currNode.minimax==MIN:
            children = []
            for availCell in currNode.grid.getAvailableCells():
                gridCopy = deepcopy(currNode.grid)
                gridCopy.insertTile(availCell, 2)
                children.append(Node([], TERM, self.getHeuristic(gridCopy), gridCopy, RAND, currNode.depth + 1))
            currNode.children = children

    def getMinimaxValue(self, root):
        stack = [root]
        while stack:
            curr = stack.pop()
            if curr.children[0].minimax!=TERM:
                childRev = curr.children.reverse()
                for child in childRev:
                    stack.append(child)
            else:
                childrenMetrics = []
                for child in curr.children:
                    childrenMetrics.append(child.metric)
                if curr.minimax==MAX:
                    curr.metric = max(childrenMetrics)
                if curr.minimax==MIN:
                    curr.metric = min(childrenMetrics)
