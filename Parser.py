
from LPolyomino import LPolyomino
from LPolyomino import LPolyomino
from RectPolyomino import RectPolyomino
from Field import Field
from utils import getSeparateLine

class Parser:

	def __init__(self) -> None:
		self.setField()
		self.__polyominoCounter = 0
		self.__lPolyominoList = []
		self.__rectPolyominoList = []
		self.setRectPolyominos()

	def setRectPolyominos(self):
		print(f"""
{getSeparateLine()}
	Enter all Rect-Polyominos:
{getSeparateLine()}""")
		while True:
			if (input("Add new? (y \ n): ") == 'n'):
				break
			self.addRectPolyomino()

	def setField(self):
		print(f"""
{getSeparateLine()}
	Enter Field parameters::
{getSeparateLine()}""")
		self.__field = Field()

	def updateId(self):
		self.__polyominoCounter += 1
		return self.__polyominoCounter

	def addRectPolyomino(self):
		height, width = tuple(map(lambda x: int(x), input("Enter height and width for a new polyomino: ").split()))
		capacity = int(input("Enter capacity: "))

		for _ in range(capacity):
			self.__rectPolyominoList.append(RectPolyomino(self.updateId(), height, width))

	def getField(self):
		return self.__field

	def getLPolyominoList(self):
		return self.__lPolyominoList

	def getRectPolyominoList(self):
		return self.__rectPolyominoList

	def getPolyominosCount(self):
		return self.__polyominoCounter