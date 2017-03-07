from random import randint
from BaseAI import BaseAI
from copy import deepcopy
from copy import copy

[TERM, MIN, MAX] = range(3)
moveIdx = [UP, DOWN, LEFT, RIGHT, RAND] = range(5)

fullBoard = []
for i in range(0,4):
    for j in range(0,4):
        fullBoard.append((i,j))

edges = set([(0,1),(0,2), (1,3), (2,3), (3,2), (3,1), (2,0), (1,0)])
corners = set([(0,0),(0,3),(3,0),(3,3)])

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
        """
        moves = grid.getAvailableMoves()
        cells = grid.getAvailableCells()
        if len(cells) < 4:
            depth = 4
        minimaxTree = self.buildMinimaxTree(grid, depth)
        """
        depth = 3
        return self.getMinimaxValue(grid, depth)

    def getHeuristic(self, grid):
        def getAdjacencyHeuristic(grid, tiledCells):
            numAdj = 0
            for currCell in tiledCells:
                for i in range(1,len(tiledCells)):
                    if grid.getCellValue(currCell)==grid.getCellValue(tiledCells[i]):
                        dist = (currCell[0] - tiledCells[i][0])**2 + (currCell[1] - tiledCells[i][1])**2
                        numAdj += float(grid.getCellValue(currCell)*(18-dist))/18
            return numAdj

        def getEdgeHeuristic(grid, tiledCells):
            edgeHeur = 0
            for cell in tiledCells:
                cellVal = grid.getCellValue(cell)
                if cellVal > 128:
                    if cell in edges:
                        edgeHeur += cellVal
                    if cell in corners:
                        edgeHeur += 2*cellVal
            return edgeHeur

        def getTiledCells(grid):
            return list(set(fullBoard) - set(grid.getAvailableCells()))

        def getAvgValue(grid, tiledCells):
            totalCellValue = 0;
            # Get total value of all cells on board
            for cell in tiledCells:
                totalCellValue += grid.getCellValue(cell)
            return float(totalCellValue) / float(len(tiledCells))


        # Copy grid
        gridCopy = grid
        tiledCells = getTiledCells(gridCopy)
        avgValue = getAvgValue(gridCopy, tiledCells)
        maxValue = gridCopy.getMaxTile()
        adjHeuristic = getAdjacencyHeuristic(gridCopy, tiledCells)
        edgeHeuristic = getEdgeHeuristic(gridCopy, tiledCells)

        # Get number of available cells
        nAvailableCells = 16 - len(tiledCells)

        print("\nMaxValue*nAvailableCells: %f" % (maxValue*nAvailableCells))
        print("AdjHeuristic: %f" % adjHeuristic)
        print("EdgeHeuristic: %f" % edgeHeuristic)
        h = maxValue*nAvailableCells + adjHeuristic + edgeHeuristic
        return h

    """
    def buildMinimaxTree(self, initGrid, depth):
        # Build root
        root = Node([], MAX, -1, initGrid, None, 0)

        # Use a queue to build tree by depth levels
        stack = [root]
        currDepth = 0
        cont = True
        while stack:
            curr = stack.pop()

            # If we're not at depth limit
            if curr.depth < depth-1:

                # Max nodes
                if curr.minimax == MAX:
                    availableMoves = curr.grid.getAvailableMoves()

                    # If there are moves available, build children and add to stack
                    if len(availableMoves) > 0:
                        self.buildMaxChildren(curr)
                        for child in curr.children[::-1]:
                            stack.append(child)

                    # If no moves available, make node terminal
                    else:
                        curr.minimax = TERM
                        curr.metric = self.getHeuristic(curr.grid)

                # Min nodes
                if curr.minimax == MIN:
                    availableCells = curr.grid.getAvailableCells()

                    # If there are cells available, build children and add to stack
                    if len(availableCells) > 0:
                        self.buildMinChildren(curr)
                        for child in curr.children[::-1]:
                            stack.append(child)

                    # If no cells available, make node terminal
                    else:
                        curr.minimax = TERM
                        curr.metric = self.getHeuristic(curr.grid)

            # If at depth limit, build terminal children
            else:
                self.buildTermChildren(curr)
        return root

            #Build tree by levels
            while depth - currDepth > 1 and cont:
                # Get next node to build
                curr = queue.pop(0)

                # If we're at the right depth
                if curr.depth == currDepth:
                    # If we're at a MAX node and there are available moves
                    if curr.minimax==MAX and len(curr.grid.getAvailableMoves()) != 0:
                        self.buildMaxChildren(curr)
                        for child in curr.children:
                            queue.append(child)
                    # If we're at a MIN node and there are available cells
                    if curr.minimax==MIN and len(curr.grid.getAvailableCells()) != 0:
                        self.buildMinChildren(curr)
                        for child in curr.children:
                            queue.append(child)
                    # If there weren't available cells or there weren't available moves,
                    # reinsert curr into the queue and break the while to build terminal children
                    if len(curr.grid.getAvailableCells()) == 0 or len(curr.grid.getAvailableMoves()) == 0:
                        queue.insert(0,curr)
                        cont = False
                # Else, this node is at next depth; reinsert into queue and increase depth
                else:
                    currDepth += 1
                    queue.insert(0,curr)

            # Once while is broke, add terminal children to all nodes in queue
            while queue:
                curr = queue.pop(0)
                self.buildTermChildren(curr)

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
        for availCell in currNode.grid.getAvailableCells():
            gridCopy = deepcopy(currNode.grid)
            gridCopy.insertTile(availCell, 4)
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
    """

    def getMinimaxValue(self, initGrid, depthLimit):
        def maximize(grid, depth):
            availMoves = grid.getAvailableMoves()

            # Terminal test
            if len(availMoves) == 0 or depth == depthLimit:
                return (grid, self.getHeuristic(grid))

            (maxChild, maxUtility) = (None, -float('inf'))
            for move in availMoves:
                movedGrid= deepcopy(grid)
                movedGrid.move(move)
                (_, utility) = minimize(movedGrid, depth + 1)
                if utility > maxUtility:
                    (maxChild, maxUtility) = (move, utility)
            return (maxChild, maxUtility)

        def minimize(grid, depth):
            availCells = grid.getAvailableCells()

            # Terminal test
            if len(availCells) == 0 or depth == depthLimit:
                return (grid, self.getHeuristic(grid))

            (minChild, minUtility) = (None, float('inf'))
            for cell in availCells:
                tilePlacedGrid= deepcopy(grid)
                tilePlacedGrid.insertTile(cell, 2)
                (_, utility) = maximize(tilePlacedGrid, depth + 1)
                if utility < minUtility:
                    (minChild, minUtility) = (RAND, utility)
            return (minChild, minUtility)
        return maximize(initGrid, 0)[0]
