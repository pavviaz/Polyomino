
from LPolyomino import LPolyomino
from LPolyomino import LPolyomino
from RectPolyomino import RectPolyomino
from Field import Field
from utils import getSeparateLine
import re

FILE_PATH = "params.txt"


class Parser:
	def __init__(self, console=False) -> None:
		self.__console = console
		self.__fieldSize = ()
		self.__RectPolyominosSize = []
		self.__LPolyominosSize = []
		if not console: 
			self.getShapesFromFile()
		self.setField()
		self.__polyominoCounter = 0
		self.__lPolyominoList = []
		self.__rectPolyominoList = []
		self.setRectPolyominos()
		self.setLPolyominos()

	def getShapesFromFile(self):
		with open(FILE_PATH) as params:
			for id, line in enumerate(params):
				if id == 0:
					self.__fieldSize = tuple(map(lambda x: int(x), [val for val in re.findall(r'\d+', line)]))
				elif id == 1:
					for fig in re.findall(r'\d+\D+\d+\D+\d+', line):
						self.__RectPolyominosSize.append([])
						for val in re.findall(r'\d+', str(fig)):
							self.__RectPolyominosSize[-1].append(int(val))
				elif id == 2:
					for fig in re.findall(r'\d+\D+\d+\D+\d+', line):
						self.__LPolyominosSize.append([])
						for val in re.findall(r'\d+', str(fig)):
							self.__LPolyominosSize[-1].append(int(val))

	def setRectPolyominos(self):
		if self.__console:
			print(f"""
{getSeparateLine()}
	Enter all Rect-Polyominos:
{getSeparateLine()}""")
			while True:
				if (input("Add new? (y \ n): ") == 'n'):
					break
				self.addRectPolyomino()
		else:
			self.addRectPolyomino()

	def setLPolyominos(self):
		if self.__console:
			print(f"""
{getSeparateLine()}
	Enter all L-Polyominos:
{getSeparateLine()}""")
			while True:
				if (input("Add new? (y \ n): ") == 'n'):
					break
				self.addLPolyomino()
		else:
			self.addLPolyomino()

	def setField(self):
		if self.__console:
			print(f"""
{getSeparateLine()}
	Enter Field parameters::
{getSeparateLine()}""")
			self.__field = Field()
		else:
			self.__field = Field(*self.__fieldSize)

	def updateId(self):
		self.__polyominoCounter += 1
		return self.__polyominoCounter

	def addRectPolyomino(self):
		if self.__console:
			height, width = tuple(map(lambda x: int(x), input("Enter height and width for a new polyomino: ").split()))
			capacity = int(input("Enter capacity: "))

			for _ in range(capacity):
				self.__rectPolyominoList.append(RectPolyomino(self.__polyominoCounter, height, width))
				self.updateId()
    
		else:
			for rect in self.__RectPolyominosSize:
				height, width, capacity = rect
    
				for _ in range(capacity):
					self.__rectPolyominoList.append(RectPolyomino(self.__polyominoCounter, height, width))
					self.updateId()

	def addLPolyomino(self):
		if self.__console:
			height, width = tuple(map(lambda x: int(x), input("Enter height and width for a new polyomino: ").split()))
			capacity = int(input("Enter capacity: "))

			for _ in range(capacity):
				self.__lPolyominoList.append(LPolyomino(self.__polyominoCounter, height, width))
				self.updateId()
	
		else:
			for lpol in self.__LPolyominosSize:
				height, width, capacity = lpol
    
				for _ in range(capacity):
					self.__lPolyominoList.append(LPolyomino(self.__polyominoCounter, height, width))
					self.updateId()


	def getField(self):
		return self.__field

	def getAllPolyominos(self):
		return self.__rectPolyominoList + self.__lPolyominoList

	def getLPolyominoList(self):
		return self.__lPolyominoList

	def getRectPolyominoList(self):
		return self.__rectPolyominoList

	def getPolyominosCount(self):
		return self.__polyominoCounter