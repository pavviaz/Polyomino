
import numpy as np
from Parser import Parser
from ortools.sat.python import cp_model

class Executor:
	def __init__(self, parser: Parser) -> None:
		self.__polyominos = parser.getRectPolyominoList()
		self.__fieldWidth, self.__fieldHeight = parser.getField().getSize()
		self.__polyominosCount = parser.getPolyominosCount()

	def getPolyominos(self):
		return self.__polyominos

	def getPolynomosCount(self):
		return self.__polyominosCount

	def createModel(self):
		self.__cpModel = cp_model.CpModel()

	def setCells(self):
		self.__cells = {
			(x, y) for x in range(self.__fieldWidth) for y in range(self.__fieldHeight)
		}

	def getCells(self):
		return self.__cells

	def setMembers(self):
		self.__members = {
			(cell, p.getId()): self.__cpModel.NewBoolVar(f"member{cell, p.getId()}")
			for cell in self.__cells
			for p in self.__polyominos
		}

	def getMembers(self):
		return self.__members

	def addConstraints(self):
		self.isNonCross()
		self.isAllPolyominosUsed()
		self.isRelativeLocated()

	def getPolyomino(self, pId):
		return self.__polyominos[pId - 1]

	# def isRelativeLocated(self):
	# 	# Find the border of each polyomino
	# 	vertices = {
	# 		v: i
	# 		for i, v in enumerate(
	# 			{(x + i, y + j) for x, y in self.__cells for i in [0, 1] for j in [0, 1]}
	# 		)
	# 	}
	# 	edges = [
	# 		edge
	# 		for x, y in self.__cells
	# 		for edge in [
	# 			((x, y), (x + 1, y)),
	# 			((x + 1, y), (x + 1, y + 1)),
	# 			((x + 1, y + 1), (x, y + 1)),
	# 			((x, y + 1), (x, y)),
	# 		]
	# 	]
	# 	border = {
	# 		(edge, p.getId()): self.__cpModel.NewBoolVar(f"border{edge, p.getId()}")
	# 		for edge in edges
	# 		for p in self.__polyominos
	# 	}

	# 	for (((x0, y0), (x1, y1)), pId), border_var in border.items():
	# 		left_cell = ((x0 + x1 + y0 - y1) // 2, (y0 + y1 - x0 + x1) // 2)
	# 		right_cell = ((x0 + x1 - y0 + y1) // 2, (y0 + y1 + x0 - x1) // 2)
	# 		left_var = self.__members[left_cell, pId]
	# 		self.__cpModel.AddBoolOr([border_var.Not(), left_var])
	# 		if (right_cell, pId) in self.__members:
	# 			right_var = self.__members[right_cell, pId]
	# 			self.__cpModel.AddBoolOr([border_var.Not(), right_var.Not()])
	# 			self.__cpModel.AddBoolOr([border_var, left_var.Not(), right_var])
	# 		else:
	# 			self.__cpModel.AddBoolOr([border_var, left_var.Not()])

	# 	# Each border is a circuit
	# 	for p in self.__polyominos:
	# 		self.__cpModel.AddCircuit(
	# 			[(vertices[v0], vertices[v1], border[(v0, v1), p.getId()]) for v0, v1 in edges]
	# 			+ [(i, i, self.__cpModel.NewBoolVar(f"vertex_loop{v, p.getId()}")) for v, i in vertices.items()]
	# 		)

	def isRelativeLocated(self):
		for (x_0, y_0), pId in self.__members:
			p = self.getPolyomino(pId)
			for x in range(p.getWidth()):
				for y in range(p.getHeight()):
					if x_0 + x < self.getFieldWidth() and y_0 + y < self.getFieldHeight():
						self.__cpModel.AddBoolOr([self.__members[(x_0, y_0), pId].Not(), self.__members[(x_0 + x, y_0 + y), pId]])

	def isNonCross(self):
		for cell in self.__cells:
			self.__cpModel.Add(sum(self.__members[cell, p.getId()] for p in self.__polyominos) < 2)

	def isAllPolyominosUsed(self):
		for p in self.__polyominos:
			self.__cpModel.Add(sum(self.__members[cell, p.getId()] for cell in self.__cells) == p.getArea())

	def configureSolver(self):
		self.createModel()
		self.setCells()
		self.setMembers()
		self.addConstraints()
		self.__solver = cp_model.CpSolver()
		self.__solutionPrinter = SolutionPrinter(self)

	def findSolution(self):
		self.__status = self.__solver.Solve(self.__cpModel, self.__solutionPrinter)

		print(f"Status = {self.__solver.StatusName(self.__status)}")
		print(f"Solutions = {self.__solutionPrinter.getSolutionsCount()}")

	def getFieldWidth(self):
		return self.__fieldWidth

	def getFieldHeight(self):
		return self.__fieldHeight

	def solve(self):
		self.configureSolver()
		self.findSolution()

	def printField(self):
		for i in range(len(self.__fieldMatrix)):
			print(*self.__fieldMatrix[i])


class SolutionPrinter(cp_model.CpSolverSolutionCallback):
	def __init__(self, outer: Executor):
		super().__init__()
		self.outer = outer
		self.__solutionsCount = 0

	def OnSolutionCallback(self):
		self.__solutionsCount += 1
		for y in range(self.outer.getFieldHeight()):
			print(
				*(
					self.getPolyominoId(x, y)
					for x in range(self.outer.getFieldWidth())
				)
			)
		print()
		if (self.__solutionsCount >= 1):
			self.StopSearch()

	def getPolyominoId(self, x ,y):
		for p in self.outer.getPolyominos():
			value = self.Value(
				self.outer.getMembers()[(x, y), p.getId()]
			)
			if value:
				return p.getId()
		return 0

	def getSolutionsCount(self):
		return self.__solutionsCount
