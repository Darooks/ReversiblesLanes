import numpy
from scipy.optimize import linprog

c = [1, 1, 1, 1, 1]
A = [[-666, -444, -222, -444, -444],
     [-444, -666, -444, -222, -444],
     [-222, -444, -666, -444, -444],
     [-444, -222, -444, -666, -444]]
b = [-1000, -50, -500, -50]  # current vehicular load
x0_b = (0, None)
x1_b = (0, None)
x2_b = (0, None)
x3_b = (0, None)
x4_b = (0, None)

# res = linprog(c, A_ub=A, b_ub=b, bounds=[x0_b, x1_b, x2_b, x3_b, x4_b], method='highs')
# for x in res.x:
#      print('{:.20f}'.format(x))
#
# myMax = numpy.where(res.x == numpy.amax(res.x)) # get index of max value
# print(myMax[0][0])


class LinearOptimizer:
    def getConfig(self, loadPerDir):
        res = linprog(c, A_ub=A, b_ub=loadPerDir, bounds=[x0_b, x1_b, x2_b, x3_b, x4_b], method='highs')
        return numpy.where(res.x == numpy.amax(res.x))
