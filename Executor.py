
import numpy as np
import matplotlib.pyplot as plt
import more_itertools as mit
from ortools.sat.python import cp_model
from JSONParser import JSONParser


class Executor:
    def __init__(self, parser: JSONParser):
        self.parser = parser
        self.model = cp_model.CpModel()
        self.pminosMtrx = [[] for _ in range(self.parser.getPolyominosCount())]

    def setVariables(self):
        for pmino in self.parser.getPolyominos():
            cells = []
            for cell in range(pmino.getArea()):
                cells.append(
                    np.array([
                        self.model.NewIntVar(0, self.parser.getField().getSize()[0] - 1, 'p%i' % pmino.getId() + 'c%i' % cell + 'x'),
                        self.model.NewIntVar(0, self.parser.getField().getSize()[1] - 1, 'p%i' % pmino.getId() + 'c%i' % cell + 'y')
                    ])
                )
            self.pminosMtrx[pmino.getId()] = [
                [
                    self.model.NewBoolVar('p%i' % pmino.getId() + 's%i' % shapeId)
                    for shapeId in range(pmino.shapesCount)
                ],
                cells
            ]

    def solve(self):
        self.setVariables()
        self.addConstraints()
        self.configureSolver()
        self.findSolution()

    def addShapesConstraint(self):
        for pmino in self.parser.getPolyominos():
            shapes, cells = self.pminosMtrx[pmino.getId()]
            topCell = cells[0]
            for shapeId in range(pmino.shapesCount):
                for cell, xy in zip(cells[1:], pmino.getShapes()[shapeId][1:]):
                    self.model.Add(cell[0] - topCell[0] == xy[0]).OnlyEnforceIf(shapes[shapeId])
                    self.model.Add(cell[1] - topCell[1] == xy[1]).OnlyEnforceIf(shapes[shapeId])
            self.model.AddBoolXOr(shapes)

    def addOverlapConstraint(self):
        cells = set(np.arange(self.parser.getField().getSize()[0] * self.parser.getField().getSize()[1]))  # Cells where polyominoes can be fitted
        ranges = [(next(g), list(g)[-1]) for g in
                  mit.consecutive_groups(cells)]  # All intervals in the stack of active cells

        cellsAddresses = []
        n = 0
        for pId, (_, cells) in enumerate(self.pminosMtrx):
            for cell in cells:
                n += 1
                cellAddress = self.model.NewIntVarFromDomain(cp_model.Domain.FromIntervals(ranges), '%i' % n)
                self.model.Add(cell[0] + cell[1] * self.parser.getField().getSize()[0] == cellAddress)
                cellsAddresses.append(cellAddress)

        self.model.AddAllDifferent(cellsAddresses)

    def addConstraints(self):
        self.addShapesConstraint()
        self.addOverlapConstraint()

    def configureSolver(self):
        self.__solver = cp_model.CpSolver()
        self.__solutionPrinter = SolutionPrinter(self.pminosMtrx, self.parser.getField())

    def findSolution(self):
        self.__status = self.__solver.Solve(self.model, self.__solutionPrinter)

        print(f"Status = {self.__solver.StatusName(self.__status)}")

        return self.__status in (cp_model.OPTIMAL, cp_model.FEASIBLE)

    def getPolynomosCount(self):
        return self.parser.getPolyominosCount()


class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    ''' Print a solution. '''

    def __init__(self, variables, field):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.variables = variables
        self.field = field
        self.count = 0

    def OnSolutionCallback(self):
        self.count += 1

        fieldSize = self.field.getSize()

        plt.figure(figsize=(2, 2))
        plt.grid(True)
        plt.axis([0, fieldSize[0], fieldSize[1], 0])
        plt.yticks(np.arange(0, fieldSize[1], 1.0))
        plt.xticks(np.arange(0, fieldSize[0], 1.0))

        for pId, (_, cells) in enumerate(self.variables):
            color = np.random.rand(3, )
            for cell in cells:
                x = self.Value(cell[0])
                y = self.Value(cell[1])
                rect = plt.Rectangle((x, y), 1, 1, facecolor=color)
                plt.gca().add_patch(rect)

        plt.show()
