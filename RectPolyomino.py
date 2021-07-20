
from Polyomino import Polyomino
import numpy as np


class RectPolyomino(Polyomino):
	def __init__(self, id, height, width):
		super().__init__(id, height, width)
		self.setShapesCount()

	def setShapesCount(self):
		self.shapesCount = 1 if self.getHeight() == self.getWidth() else 2

	def getArea(self):
		return self.getHeight() * self.getWidth()

	def getShapes(self):
		shapes = np.array([[np.array((x, y)) for y in range(self.getHeight()) for x in range(self.getWidth())]])
		if self.shapesCount > 1:
			shapes = np.append(
				shapes,
				[[np.array((x, y)) for y in range(self.getWidth()) for x in range(self.getHeight())]],
				axis=0
			)
		return shapes
