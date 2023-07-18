from FuzzyDetector import FuzzyDetector
from LinearOptimizer import LinearOptimizer
import utils


def get_road_load(traci):
    curr_vehicles = traci.vehicle.getIDList()
    load_road_cnts = dict()   # counters of vehicles for North, East, South, West roads
    result = []

    for direction in utils.GEO_DIRS:
        load_road_cnts[direction] = 0

    for veh_id in curr_vehicles:
        lane_id = traci.vehicle.getLaneID(veh_id)
        lane_id = lane_id.split('_')
        if lane_id[2] != "start":
            ''' Analyzing the start lanes only. Intersection and end lanes are not needed. '''
            continue
        load_road_cnts[lane_id[0]] += 1

    for direction in utils.GEO_DIRS:
        result.append(load_road_cnts[direction])

    return result


def get_avg_speed(traci):
    curr_vehicles = traci.vehicle.getIDList()
    avg_speed_per_lane = dict()
    veh_cnt = dict()

    for veh_id in curr_vehicles:
        lane_id = traci.vehicle.getLaneID(veh_id)
        if lane_id.split('_')[2] != "start":
            ''' Analyzing the start lanes only. Intersection and end lanes are not needed. '''
            continue
        if lane_id not in avg_speed_per_lane.keys():
            avg_speed_per_lane[lane_id] = traci.vehicle.getSpeed(veh_id)
            veh_cnt[lane_id] = 1
        else:
            avg_speed_per_lane[lane_id] += traci.vehicle.getSpeed(veh_id)
            veh_cnt[lane_id] += 1

    for lane_id in avg_speed_per_lane.keys():
        avg_speed_per_lane[lane_id] = 3.6 * (avg_speed_per_lane[lane_id] / veh_cnt[lane_id])

    return avg_speed_per_lane


def get_density(traci):
    density_per_lane = dict()  # lane_id -> veh_cnt
    curr_vehicles = traci.vehicle.getIDList()

    for veh_id in curr_vehicles:
        lane_id = traci.vehicle.getLaneID(veh_id)
        if lane_id.split('_')[2] != "start":
            ''' Analyzing the start lanes only. Intersection and end lanes are not needed. '''
            continue
        if lane_id not in density_per_lane.keys():
            density_per_lane[lane_id] = 1
        else:
            density_per_lane[lane_id] += 1

    return density_per_lane


class Manager:
    def __init__(self):
        self.fd = FuzzyDetector()
        self.lo = LinearOptimizer()
        self.veh_ln_cnts = dict()
        for n in utils.DIRECTIONS:
            self.veh_ln_cnts[n] = 0

    def _reset_veh_ln_cnts(self):
        for dir in utils.DIRECTIONS:
            self.veh_ln_cnts[dir] = 0

    def _count_veh_on_lanes(self, traci):
        curr_vehicles = traci.vehicle.getIDList()

        self._reset_veh_ln_cnts()
        for veh_id in curr_vehicles:
            route_id = traci.vehicle.getRouteID(veh_id)  # traci.vehicle.getLaneID
            if route_id in utils.DIRECTIONS:
                self.veh_ln_cnts[route_id] += 1

    def is_cngst_too_high(self, traci, verbose=False):
        avg_speed_lane = get_avg_speed(traci)
        density_lane = get_density(traci)
        cngst_lvl = -1

        for lane_id in avg_speed_lane.keys():
            cngst_lvl = max(cngst_lvl, self.fd.get_cngst_lvl(avg_speed_lane[lane_id], density_lane[lane_id]))

        if verbose:
            print("Congestion level =", cngst_lvl)
        if cngst_lvl >= 4.0:
            return True
        return False

    def simulationStep(self, traci, verbose=False):
        # self._count_veh_on_lanes(traci)
        # print(self.veh_ln_cnts)
        if verbose:
            print("Actual road traffic =", get_road_load(traci))

        if self.is_cngst_too_high(traci, verbose) is not True:
            return None

        current_load = get_road_load(traci)
        config_index = self.lo.get_config_index(current_load)

        if verbose:
            print("Config:", utils.CONFIGURATIONS[config_index], "Current Load:", current_load)
        return config_index

