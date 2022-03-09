import numpy as np
import time
import more_itertools as mit
from Parser import Parser
from ortools.sat.python import cp_model


class Executor:
    def __init__(self, parser: Parser):
        self.parser = parser
        self.model = cp_model.CpModel()   # инициализация CP-SAT
        self.pminosMtrx = [[] for _ in range(self.parser.getPolyominosCount())]

    def setVariables(self):
        # создание матриц из координат фигур
        for pmino in self.parser.getAllPolyominos():
            cells = []
            for cell in range(pmino.getArea()):  
                cells.append(
                    np.array([
                        self.model.NewIntVar(0, self.parser.getField().getSize()[0] - 1, 'p%i' % pmino.getId() + 'c%i' % cell + 'x'),
                        self.model.NewIntVar(0, self.parser.getField().getSize()[1] - 1, 'p%i' % pmino.getId() + 'c%i' % cell + 'y')
                    ])
                )
            self.pminosMtrx[pmino.getId()] = [   # создание матрицы из координат фигур 
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
        return self.findSolution()

    def addShapesConstraint(self):
        # добавление ограничений для форм фигур
        for pmino in self.parser.getAllPolyominos():
            shapes, cells = self.pminosMtrx[pmino.getId()]
            topCell = cells[0]
            for shapeId in range(pmino.shapesCount):
                for cell, xy in zip(cells[1:], pmino.getShapes()[shapeId][1:]):
                    self.model.Add(cell[0] - topCell[0] == xy[0]).OnlyEnforceIf(shapes[shapeId])
                    self.model.Add(cell[1] - topCell[1] == xy[1]).OnlyEnforceIf(shapes[shapeId])
            self.model.AddBoolXOr(shapes)

    def addOverlapConstraint(self):
        # добавление ограничений для наложения фигур
        cells = set(np.arange(self.parser.getField().getSize()[0] * self.parser.getField().getSize()[1]))  # Cells where polyominoes can be fitted
        ranges = [(next(g), list(g)[-1]) for g in
                  mit.consecutive_groups(cells)]  # All intervals in the stack of active cells

        cellsAddresses = []
        n = 0
        for _, (_, cells) in enumerate(self.pminosMtrx):
            for cell in cells:
                n += 1
                cellAddress = self.model.NewIntVarFromDomain(cp_model.Domain.FromIntervals(ranges), '%i' % n)
                self.model.Add(cell[0] + cell[1] * self.parser.getField().getSize()[0] == cellAddress)
                cellsAddresses.append(cellAddress)

        self.model.AddAllDifferent(cellsAddresses)

    def addConstraints(self):
        # добавление огриничений
        self.addShapesConstraint()
        self.addOverlapConstraint()

    def configureSolver(self):
        # создания экземпляра класса "решателя" SAT
        self.__solver = cp_model.CpSolver()

    def findSolution(self):
        # запуск "решателя" 
        cur_time = time.time()
        self.__status = self.__solver.Solve(self.model)
        print(self.__status in (cp_model.OPTIMAL, cp_model.FEASIBLE)) 
        return time.time() - cur_time

    def getPolyominos(self):
        return self.parser.getRectPolyominoList()

    def getPolyomino(self, pId):
        return self.getPolyominos()[pId - 1]
