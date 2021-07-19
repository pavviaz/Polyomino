
from Executor import Executor
from Parser import Parser

parser = Parser()
parser.getField().info()
for polyomino in parser.getLPolyominoList() + parser.getRectPolyominoList():
	polyomino.info()

executor = Executor(parser)
executor.solve()