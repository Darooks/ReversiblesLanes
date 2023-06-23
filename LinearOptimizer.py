import numpy
from scipy.optimize import linprog
from utils import *
import random
import sys
import warnings


class LinearOptimizer:
    def __init__(self):
        self.c = [1, 1, 1]
        self.A = [[-2, -3, -1],
                  [-2, -1, -3]]
        self.x_bounds = [(0, None), (0, None), (0, None)]  # x bound for utils.CONFIGURATIONS

    def get_config_index(self, load_per_dir):
        norm_load = [n * (-1) for n in load_per_dir]  # we want to maximize so multiply by -1 all values
        x_all = [0]*len(DIRECTION)

        result = linprog(self.c,
                         A_ub=self.A,
                         b_ub=[norm_load[DIRECTION.NORTH.value], norm_load[DIRECTION.SOUTH.value]],
                         bounds=self.x_bounds,
                         method='highs')
        xd_temp, x_all[DIRECTION.NORTH.value], x_all[DIRECTION.SOUTH.value] = result.x

        result = linprog(self.c,
                         A_ub=self.A,
                         b_ub=[norm_load[DIRECTION.EAST.value], norm_load[DIRECTION.WEST.value]],
                         bounds=self.x_bounds,
                         method='highs')
        xd, x_all[DIRECTION.EAST.value], x_all[DIRECTION.WEST.value] = result.x
        x_all[DIRECTION.DEFAULT.value] = max(xd_temp, xd)

        return x_all.index(max(x_all))
