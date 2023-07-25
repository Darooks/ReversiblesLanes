from scipy.optimize import linprog
import sys
sys.path.append('C:\\Projects\\SUMO-SIMULATOR\\ReversibleLanesIntersection')
from utils import *


class LinearOptimizer:
    def __init__(self):
        self.c = [1, 1, 1]
        self.A = [[-2, -3, -1],
                  [-2, -1, -3]]
        self.x_bounds = [(0, None), (0, None), (0, None)]  # x bound for utils.CONFIGURATIONS

    def get_config_index(self, load_per_dir, verbose=False):
        norm_load = [n * (-1) for n in load_per_dir]  # we want to maximize so multiply by -1 all values
        norm_load.insert(DIRECTION.DEFAULT.value, 0)
        x_all = [0]*len(DIRECTION)
        index = DIRECTION.DEFAULT.value

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
        x_all = [int(n) for n in x_all]

        if x_all.count(max(x_all)) == 1:
            index = x_all.index(max(x_all))

        if verbose is True:
            print("X bounds:")
            print("\t xd_temp =", xd_temp)
            print("\t xd =", xd)
            print("\t x_default =", x_all[DIRECTION.DEFAULT.value])
            print("\t x_north =", x_all[DIRECTION.NORTH.value])
            print("\t x_east =", x_all[DIRECTION.EAST.value])
            print("\t x_south =", x_all[DIRECTION.SOUTH.value])
            print("\t x_west =", x_all[DIRECTION.WEST.value])
            print("\t Selected index =", index)

        return index
