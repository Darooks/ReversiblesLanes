from utils import DIRECTION, GEO_DIRS
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

        for geo_dir in GEO_DIRS:
            r = random.randint(1, 10)
            if geo_dir == self.dir:
                if r <= 5:
                    route_id = get_random_route_from_src(geo_dir)
                    vid = "v.%s.%d.%d" % (route_id, step, id_cnt)
                    traci.vehicle.add(vid, route_id, typeID="vtypeauto")
                    id_cnt += 1
                continue

            if r <= 2:
                route_id = get_random_route_from_src(geo_dir)
                vid = "v.%s.%d.%d" % (route_id, step, id_cnt)
                traci.vehicle.add(vid, route_id, typeID="vtypeauto")
                id_cnt += 1

    def simulationStep(self, traci, step):
        if self.type == "balanced":
            self.balanced_load(traci, step)
        elif self.type == "wave":
            self.balanced_load(traci, step, self.dir)
