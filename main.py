
from Executor import Executor
from Parser import Parser

parser = Parser()
parser.getField().info()
for polyomino in parser.getAllPolyominos():
	polyomino.info()

executor = Executor(parser)
executor.solve()