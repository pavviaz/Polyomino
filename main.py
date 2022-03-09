
import argparse
import random
from matplotlib import pyplot as plt
from Executor import Executor
from Parser import Parser

TEST_COUNT = 5
times = []

def randomParams(i):
    lpol = []
    rpol = []
    field = (random.randint(3*i, 3*i+10), random.randint(3*i, 3*i+10))
    for _ in range(random.randint(1, 4)):
        rpol.append(((random.randint(2*i + 3, 2*i + 7), random.randint(2*i + 3, 2*i + 7)), random.randint(1, 3)))
    for _ in range(random.randint(1, 4)):
        lpol.append(((random.randint(2*i + 3, 2*i + 7), random.randint(2*i + 1, 2*i + 2)), random.randint(1, 3)))
    with open("params.txt", "w+") as params:
        params.write(f"{str(field)}\n{str(rpol)}\n{str(lpol)}")
        
argparser = argparse.ArgumentParser(description='Forked script for polyomino tiling problem', add_help=True)
argparser.add_argument('-c', '--console', action='store_true', help='Use console for figures shapes input')
argparser.add_argument('-t', '--tests', action='store_true', help='Make some tests')

if argparser.parse_args().tests:
    for i in range(TEST_COUNT):
        randomParams(i)
        parser = Parser(argparser.parse_args().console)

        executor = Executor(parser)
        times.append(executor.solve())
    
    plt.plot(list(range(TEST_COUNT)), times)
    plt.show()
else:
    parser = Parser(argparser.parse_args().console)

    executor = Executor(parser)
    executor.solve()
    
