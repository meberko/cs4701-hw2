from BaseAI import BaseAI
from copy import deepcopy
from copy import copy
import time

moveIdx = [UP, DOWN, LEFT, RIGHT, RAND] = range(5)

fullBoard = []
for i in range(0,4):
    for j in range(0,4):
        fullBoard.append((i,j))

edges = set([(0,1),(0,2), (1,3), (2,3), (3,2), (3,1), (2,0), (1,0)])
corners = set([(0,0),(0,3),(3,0),(3,3)])
timeLimit = 0.2
gradientMap = [[64,32,16,8],[32,16,8,4], [16,8,4,2], [8,4,2,1]]

class PlayerAI(BaseAI):
    def getMove(self, grid):
        depth = 3
        if len(grid.getAvailableCells()) < 5:
            depth = 4
        if len(grid.getAvailableCells()) < 4:
            depth = 5
        if len(grid.getAvailableCells()) < 2:
            depth = 6
        return self.getMinimaxValue(grid, depth)

    def getHeuristic(self, grid):
        def getAdjacencyHeuristic(grid, tiledCells):
            numAdj = 0
            for currCell in tiledCells:
                for i in range(1,len(tiledCells)):
                    if grid.getCellValue(currCell)==grid.getCellValue(tiledCells[i]):
                        dist = abs(currCell[0] - tiledCells[i][0]) + abs(currCell[1] - tiledCells[i][1])
                        if dist == 1:
                            numAdj += (grid.getCellValue(currCell)**2)*(2**(6-dist))
                        #else:
                        #    numAdj += grid.getCellValue(currCell)*(2**(6-dist))
            return numAdj

        def getEdgeHeuristic(grid, tiledCells):
            edgeHeur = 0
            for cell in tiledCells:
                cellVal = grid.getCellValue(cell)
                if cellVal > 64:
                    if cell in edges:
                        edgeHeur += cellVal
                    if cell in corners:
                        edgeHeur += cellVal*10
                else:
                    if cell in edges:
                        edgeHeur -= cellVal/2
                    if cell in corners:
                        edgeHeur -= (cellVal/2)**2
            return edgeHeur

        def getGradientHeuristic(grid, tiledCells):
            gradHeur = 0
            for cell in tiledCells:
                i = cell[0]
                j = cell[1]
                gradHeur += gradientMap[i][j]*grid.getCellValue(cell)
            return gradHeur

        def getTiledCells(grid):
            return list(set(fullBoard) - set(grid.getAvailableCells()))


        def getAvgValue(grid, tiledCells):
            totalCellValue = 0;
            # Get total value of all cells on board
            for cell in tiledCells:
                totalCellValue += grid.getCellValue(cell)
            return float(totalCellValue) / float(len(tiledCells))


        maxValue = grid.getMaxTile()
        tiledCells = getTiledCells(grid)
        avgValue = getAvgValue(grid, tiledCells)
        adjHeuristic = getAdjacencyHeuristic(grid, tiledCells)
        edgeHeuristic = getEdgeHeuristic(grid, tiledCells)
        gradHeuristic = getGradientHeuristic(grid, tiledCells)


        # Get number of available cells
        nAvailableCells = 16 - len(tiledCells)
        print("\nmaxValue*(2**nAvailableCells): %f" % (maxValue*(2**nAvailableCells)))
        print("AvgValue*100: %f" % (avgValue*100))
        print("AdjHeuristic: %f" % adjHeuristic)
        print("EdgeHeuristic: %f" % edgeHeuristic)
        print("GradHeuristic: %f" % gradHeuristic)
        h = 10*maxValue*(2**nAvailableCells) + 100*avgValue + adjHeuristic + edgeHeuristic
        return h

    def getMinimaxValue(self, initGrid, depthLimit):
        def checkTime(start):
            if time.clock() - start > timeLimit:
                return True
            return False

        def maximize(grid, depth, alpha, beta, startTime):
            availMoves = grid.getAvailableMoves()

            # Terminal test
            if len(availMoves) == 0 or depth == depthLimit or checkTime(startTime):
                return (grid, self.getHeuristic(grid))

            (maxChild, maxUtility) = (None, -float('inf'))
            for move in availMoves:
                movedGrid= deepcopy(grid)
                movedGrid.move(move)
                (_, utility) = minimize(movedGrid, depth + 1, alpha, beta, startTime)

                if utility > maxUtility:
                    (maxChild, maxUtility) = (move, utility)

                if maxUtility >= beta:
                    break
                alpha = max(alpha, maxUtility)
            return (maxChild, maxUtility)

        def minimize(grid, depth, alpha, beta, startTime):
            availCells = grid.getAvailableCells()

            # Terminal test
            if len(availCells) == 0 or depth == depthLimit:
                return (grid, self.getHeuristic(grid))

            (minChild, minUtility) = (None, float('inf'))
            for cell in availCells:
                tilePlacedGrid= deepcopy(grid)
                tilePlacedGrid.insertTile(cell, 2)
                (_, utility) = maximize(tilePlacedGrid, depth + 1, alpha, beta, startTime)
                if utility < minUtility:
                    (minChild, minUtility) = (RAND, utility)
                if minUtility <= alpha:
                    break
                beta = min(beta, minUtility)
            """
            for cell in availCells:
                tilePlacedGrid= deepcopy(grid)
                tilePlacedGrid.insertTile(cell, 4)
                (_, utility) = maximize(tilePlacedGrid, depth + 1, alpha, beta)
                if utility < minUtility:
                    (minChild, minUtility) = (RAND, utility)
            """
            return (minChild, minUtility)

        return maximize(initGrid, 0, -float('inf'), float('inf'), time.clock())[0]
