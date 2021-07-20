
from Executor import Executor
from JSONParser import JSONParser

parser = JSONParser("config.json")
parser.parse()

executor = Executor(parser)
executor.solve()
