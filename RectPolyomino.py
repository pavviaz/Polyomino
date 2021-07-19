
from Polyomino import Polyomino

class RectPolyomino(Polyomino):
	def __init__(self, id, height, width) -> None:
		super().__init__(id, height, width)

	def getPossibleShapes(self):
		shapes = []

		shapes.append({
			(x, y) for x in range(self.getWidth()) for y in range(self.getHeight())
		})
		if (self.getHeight() != self.getWidth()):
			shapes.append({
				(x, y) for x in range(self.getWidth()) for y in range(self.getHeight())
			})
		return shapes