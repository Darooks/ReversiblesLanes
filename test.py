import numpy
from scipy.optimize import linprog
import utils
import random
import sys
import warnings
from LinearOptimizer import LinearOptimizer

warnings.filterwarnings("ignore")
c = [1, 1, 1]

A = [
    [-2, -3, -1],
    [-2, -1, -3]
]

lp = LinearOptimizer()

while True:
    load = [random.randint(0, 222) for n in range(4)]
    # load = [20, 20, 0, 0]
    print("load:", load)
    index = lp.get_config_index(load, True)
    print("result:", utils.CONFIGURATIONS[index])
    print("press a key\n\n\n\n")
    sys.stdin.read(1)

# show me result of [87, 100, 32, 51]
# it is north, i am wondering if it should be default

# while True:
#     load = [-51, -116, -63, -145]
#
#     xd = (0, None)  # Default config
#     xd_temp = (0, None)
#     xn = (0, None)  # North config
#     xe = (0, None)  # East config
#     xs = (0, None)  # South config
#     xw = (0, None)  # West config
#
#     b = [load[utils.DIRECTION.NORTH.value], load[utils.DIRECTION.SOUTH.value]]
#     result = linprog(c, A_ub=A, b_ub=b, bounds=[xd_temp, xn, xs], method='highs')  # interior-point
#     xd_temp, xn, xs = result.x
#
#     print("load:", load, "\n")
#
#     b = [load[utils.DIRECTION.EAST.value], load[utils.DIRECTION.WEST.value]]
#     result = linprog(c, A_ub=A, b_ub=b, bounds=[xd, xe, xw], method='highs')
#     xd, xe, xw = result.x
#
#     xd = max(xd_temp, xd)
#
#     x_all = [xd, xn, xe, xs, xw]
#     index = 0
#     for x in x_all:
#         print(utils.CONFIGURATIONS[index], x)
#         index += 1
#
#     print("press a key\n\n\n\n")
#     # sys.stdin.read(1)
#     break
