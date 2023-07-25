from utils import GEO_DIRS
import random


def get_random_route() -> str:
    source = random.choice(GEO_DIRS)
    destination_list = GEO_DIRS
    destination_list.remove(source)
    destination = random.choice(destination_list)
    route = source + '_' + destination
    return route


def get_random_route_from_src(source) -> str:
    destination_list = [d for d in GEO_DIRS]
    destination_list.remove(source)
    destination = random.choice(destination_list)
    route = source + '_' + destination
    return route


def add_vehicle_fixed_route(traci, step: int):
    id_cnt = 0
    route_id = "north_south"
    vid = "v.%s.%d.%d" % (route_id, step, id_cnt)
    traci.vehicle.add(vid, route_id, typeID="vtypeauto")

    # route_id = "north_west"
    # vid = "v.%s.%d" % (route_id, step)
    # traci.vehicle.add(vid, route_id, typeID="vtypeauto")
    #
    # route_id = "north_east"
    # vid = "v.%s.%d" % (route_id, step)
    # traci.vehicle.add(vid, route_id, typeID="vtypeauto")

    # route_id = "east_west"
    # vid = "v.%s.%d" % (route_id, step)
    # traci.vehicle.add(vid, route_id, typeID="vtypeauto")

class TrafficGenerator():
    def set_dir(self, dir):
        if dir in GEO_DIRS:
            self.dir = dir
        else:
            print("ERROR: unknown source direction.")

    def __init__(self, type="balanced", dir="north"):
        self.type = type
        self.dir = dir

    def balanced_load(self, traci, step):
        id_cnt = 0

        for src in GEO_DIRS:
            r = random.randint(1, 4)
            if r <= 2:
                route_id = get_random_route_from_src(src)
                vid = "v.%s.%d.%d" % (route_id, step, id_cnt)
                traci.vehicle.add(vehID=vid, routeID=route_id, typeID="vtypeauto")
                id_cnt += 1

    def wave_load(self, traci, step):
        id_cnt = 0
        route_id = str()

        r = random.randint(1, 100)
        if r <= 90:
            route_id = get_random_route_from_src('north')
        elif 90 < r <= 96:
            route_id = get_random_route_from_src('south')
        elif 96 < r <= 98:
            route_id = get_random_route_from_src('east')
        elif 98 < r <= 100:
            route_id = get_random_route_from_src('west')

        vid = "v.%s.%d.%d" % (route_id, step, id_cnt)
        traci.vehicle.add(vehID=vid, routeID=route_id, typeID="vtypeauto")
        id_cnt += 1

    def fixed_wave_load(self, traci, step):
        id_cnt = 0
        route_id = str()

        # for src in GEO_DIRS:
        r = random.randint(1, 100)
        if r <= 90:
            route_id = "north_south"
        elif 90 < r <= 96:
            route_id = "south_north"
        elif 96 < r <= 98:
            route_id = "east_west"
        elif 98 < r <= 100:
            route_id = "west_east"

        print("ROUTE ID", route_id)

        vid = "v.%s.%d.%d" % (route_id, step, id_cnt)
        traci.vehicle.add(vehID=vid, routeID=route_id, typeID="vtypeauto")
        id_cnt += 1

    def simulationStep(self, traci, step):
        if step % 100 != 0:
            return

        if self.type == "balanced":
            self.balanced_load(traci, step)
        elif self.type == "wave":
            self.wave_load(traci, step)
        elif self.type == "fixed_wave":
            self.fixed_wave_load(traci, step)
