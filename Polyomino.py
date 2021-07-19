
from utils import getSeparateLine

class Polyomino:
	def __init__(self, id, height, width) -> None:
		self.__id = id
		self.setSize(height, width)

	def getName(self):
		return self.__class__.__name__ + ' #' + str(self.__id)

	def setSize(self, height, width):
		self.__height, self.__width = height, width

	def getId(self):
		return self.__id

	def getArea(self):
		return self.__height * self.__width

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