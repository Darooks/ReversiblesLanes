import numpy
from scipy.optimize import linprog
import utils
import random
import sys
import warnings
from LinearOptimizer import LinearOptimizer
from FuzzyDetector import FuzzyDetector

def validate_linear_optimizer():
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
