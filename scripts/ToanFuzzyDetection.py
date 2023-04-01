from fuzzylogic.classes import Domain, Set, Rule
from fuzzylogic.hedges import very
from fuzzylogic.functions import R, S, alpha, trapezoid
from matplotlib import pyplot
pyplot.rc("figure", figsize=(10, 10))

MAX_AVG_SPEED = 120
MAX_VEH_DENSITY = 60


class FuzzyDetection:
    def plot_avg_speed_domain(self):
        self.avg_speed.very_low.plot()
        self.avg_speed.low.plot()
        self.avg_speed.medium.plot()
        self.avg_speed.high.plot()
        self.avg_speed.very_high.plot()

        x = [25, 60, 80, 100, 120]
        pyplot.xticks(x)
        pyplot.xlabel('Prędkość [km/h]')
        pyplot.ylabel('Współczynnik [μ]')
        pyplot.title('Rozmyta partycja dla domeny prędkości')
        pyplot.legend(['Bardzo niska', 'Niska', 'Średnia', 'Wysoka', 'Bardzo wysoka'])
        pyplot.savefig('speed_fuzzy_rules_toan21.pdf')
        pyplot.show()
        pyplot.clf()

    def plot_density_domain(self):
        self.density.low.plot()
        self.density.very_low.plot()
        self.density.medium.plot()
        self.density.high.plot()
        self.density.very_high.plot()

        x = [7, 20, 30, 45, 60]
        pyplot.xticks(x)
        pyplot.xlabel('Gęstość [poj./km]')
        pyplot.ylabel('Współczynnik [μ]')
        pyplot.title('Rozmyta partycja dla domeny gęstości')
        pyplot.legend(['Bardzo niska', 'Niska', 'Średnia', 'Wysoka', 'Bardzo wysoka'])
        pyplot.savefig('density_fuzzy_rules_toan21.pdf')
        pyplot.show()
        pyplot.clf()

    def plot_cngst(self):
        self.cngst_lvl.very_heavy.plot()
        self.cngst_lvl.heavy.plot()
        self.cngst_lvl.moderate.plot()
        self.cngst_lvl.light.plot()
        self.cngst_lvl.free_flow.plot()

        pyplot.show()
        pyplot.clf()

    def __init__(self):
        self.avg_speed = Domain("speed", 0, MAX_AVG_SPEED + 10, res=1)
        self.avg_speed.very_low = S(25, 60)
        self.avg_speed.low = alpha(floor=0, ceiling=1, func=trapezoid(25, 60, 60, 80))
        self.avg_speed.medium = alpha(floor=0, ceiling=1, func=trapezoid(60, 80, 80, 100))
        self.avg_speed.high = alpha(floor=0, ceiling=1, func=trapezoid(80, 100, 100, 120))
        self.avg_speed.very_high = R(100, MAX_AVG_SPEED)

        self.density = Domain("density", 0, MAX_VEH_DENSITY + 10, res=1)
        self.density.very_low = S(7, 20)
        self.density.low = alpha(floor=0, ceiling=1, func=trapezoid(7, 20, 20, 30))
        self.density.medium = alpha(floor=0, ceiling=1, func=trapezoid(20, 30, 30, 45))
        self.density.high = alpha(floor=0, ceiling=1, func=trapezoid(30, 45, 45, 60))
        self.density.very_high = R(45, MAX_VEH_DENSITY)

        self.cngst_lvl = Domain("congestion level", 0, 40)
        self.cngst_lvl.free_flow = S(0, 5)
        self.cngst_lvl.light = alpha(floor=0, ceiling=1, func=trapezoid(5, 10, 10, 15))
        self.cngst_lvl.moderate = alpha(floor=0, ceiling=1, func=trapezoid(15, 20, 20, 25))
        self.cngst_lvl.heavy = alpha(floor=0, ceiling=1, func=trapezoid(25, 30, 30, 35))
        self.cngst_lvl.very_heavy = R(35, 40)

        # self.rules = self._set_rules()


fd = FuzzyDetection()
fd.plot_avg_speed_domain()
fd.plot_density_domain()