
from Executor import Executor
from JSONParser import JSONParser

parser = JSONParser("config1.json")
parser.parse()

parser.getField().info()
for p in parser.getPolyominos():
    p.info()

executor = Executor(parser)
answer = executor.solve()

print(f"Answer: {answer}")