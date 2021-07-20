
from utils import getSeparateLine


class Polyomino:
	def __init__(self, id, height, width) -> None:
		self.__id = id
		self.shapesCount = 0
		self.__width = width
		self.__height = height

	def getName(self):
		return self.__class__.__name__ + ' #' + str(self.__id)

	def getId(self):
		return self.__id

	def getWidth(self):
		return self.__width

	def getHeight(self):
		return self.__height

	def info(self):
		print(f"""{getSeparateLine()}
{self.getName()}:
	- width: {self.__width}
	- heigth: {self.__height}
{getSeparateLine()}""")