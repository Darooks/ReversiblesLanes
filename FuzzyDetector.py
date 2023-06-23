from fuzzylogic.classes import Domain, Set, Rule
from fuzzylogic.hedges import very
from fuzzylogic.functions import R, S, alpha, trapezoid
from matplotlib import pyplot
pyplot.rc("figure", figsize=(10, 10))

MAX_AVG_SPEED = 50
MAX_VEH_DENSITY = 222


class FuzzyDetector:
    def _set_rules(self):
        return Rule({(self.avg_speed.very_low, self.density.very_high): self.cngst_lvl.very_heavy,
                     (self.avg_speed.very_low, self.density.high): self.cngst_lvl.very_heavy,
                     (self.avg_speed.very_low, self.density.medium): self.cngst_lvl.very_heavy,
                     (self.avg_speed.low, self.density.very_high): self.cngst_lvl.very_heavy,
                     (self.avg_speed.low, self.density.high): self.cngst_lvl.heavy,
                     (self.avg_speed.low, self.density.medium): self.cngst_lvl.moderate,
                     (self.avg_speed.low, self.density.low): self.cngst_lvl.moderate,
                     (self.avg_speed.medium, self.density.very_high): self.cngst_lvl.heavy,
                     (self.avg_speed.medium, self.density.high): self.cngst_lvl.heavy,
                     (self.avg_speed.medium, self.density.medium): self.cngst_lvl.moderate,
                     (self.avg_speed.medium, self.density.low): self.cngst_lvl.light,
                     (self.avg_speed.medium, self.density.very_low): self.cngst_lvl.light,
                     (self.avg_speed.high, self.density.high): self.cngst_lvl.moderate,
                     (self.avg_speed.high, self.density.medium): self.cngst_lvl.moderate,
                     (self.avg_speed.high, self.density.low): self.cngst_lvl.light,
                     (self.avg_speed.high, self.density.very_low): self.cngst_lvl.free_flow,
                     (self.avg_speed.very_high, self.density.medium): self.cngst_lvl.light,
                     (self.avg_speed.very_high, self.density.low): self.cngst_lvl.free_flow,
                     (self.avg_speed.very_high, self.density.very_low): self.cngst_lvl.free_flow,
                     })

    def plot_avg_speed_domain(self):
        self.avg_speed.very_low.plot()
        self.avg_speed.low.plot()
        self.avg_speed.medium.plot()
        self.avg_speed.high.plot()
        self.avg_speed.very_high.plot()

        pyplot.xlabel('Prędkość [km/h]')
        pyplot.ylabel('Współczynnik [μ]')
        pyplot.title('Rozmyta partycja dla domeny prędkości')
        pyplot.legend(['Bardzo niska', 'Niska', 'Średnia', 'Wysoka', 'Bardzo wysoka'])
        pyplot.savefig('speed_fuzzy_rules.pdf')
        pyplot.show()
        pyplot.clf()

    def plot_density_domain(self):
        self.density.low.plot()
        self.density.very_low.plot()
        self.density.medium.plot()
        self.density.high.plot()
        self.density.very_high.plot()

        x = [25, 74, 111, 166, 222]
        pyplot.xticks(x)
        pyplot.xlabel('Gęstość [poj./km]')
        pyplot.ylabel('Współczynnik [μ]')
        pyplot.title('Rozmyta partycja dla domeny gęstości')
        pyplot.legend(['Bardzo niska', 'Niska', 'Średnia', 'Wysoka', 'Bardzo wysoka'])
        pyplot.savefig('density_fuzzy_rules.pdf')
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

    def get_cngst_lvl(self, avg_speed, density):
        if avg_speed is None:
            avg_speed = 0
        if density is None:
            density = 0

        values = {self.avg_speed: avg_speed, self.density: density}
        result = self.rules(values)

        if result is None:
            return -1
        elif result <= 5:
            return 1
        elif result <= 15:
            return 2
        elif result <= 25:
            return 3
        elif result <= 35:
            return 4
        else:
            return 5

    def __init__(self):
        self.avg_speed = Domain("speed", 0, MAX_AVG_SPEED + 10, res=1)
        self.avg_speed.very_low = S(10, 20)
        self.avg_speed.low = alpha(floor=0, ceiling=1, func=trapezoid(10, 20, 20, 30))
        self.avg_speed.medium = alpha(floor=0, ceiling=1, func=trapezoid(20, 30, 30, 40))
        self.avg_speed.high = alpha(floor=0, ceiling=1, func=trapezoid(30, 40, 40, 50))
        self.avg_speed.very_high = R(40, MAX_AVG_SPEED)

        self.density = Domain("density", 0, MAX_VEH_DENSITY + 10, res=1)
        self.density.very_low = S(25, 74)
        self.density.low = alpha(floor=0, ceiling=1, func=trapezoid(25, 74, 74, 111))
        self.density.medium = alpha(floor=0, ceiling=1, func=trapezoid(74, 111, 111, 166))
        self.density.high = alpha(floor=0, ceiling=1, func=trapezoid(111, 166, 166, 222))
        self.density.very_high = R(166, MAX_VEH_DENSITY)

        self.cngst_lvl = Domain("congestion level", 0, 40)
        self.cngst_lvl.free_flow = S(0, 5)
        self.cngst_lvl.light = alpha(floor=0, ceiling=1, func=trapezoid(5, 10, 10, 15))
        self.cngst_lvl.moderate = alpha(floor=0, ceiling=1, func=trapezoid(15, 20, 20, 25))
        self.cngst_lvl.heavy = alpha(floor=0, ceiling=1, func=trapezoid(25, 30, 30, 35))
        self.cngst_lvl.very_heavy = R(35, 40)

        self.rules = self._set_rules()


# fd = FuzzyDetector()
# fd.plot_cngst()
# fd.plot_density_domain()
# print(fd.get_cngst_lvl(10, 166))
# print(fd.get_cngst_lvl(50, 25))
# print(fd.get_cngst_lvl(35, 100))
# print(fd.get_cngst_lvl(60, 40))
# print(fd.get_cngst_lvl(50, 80))
