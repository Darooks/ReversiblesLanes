import traci
from utils import *
from datetime import datetime
import os
from Manager import Manager

CONFIGURATIONS = {
    DIRECTION.DEFAULT: 'cfg/default_configuration/default.sumo.cfg',
    DIRECTION.NORTH: 'cfg/n_configuration/n.sumo.cfg',
    DIRECTION.WEST: 'cfg/w_configuration/w.sumo.cfg',
    DIRECTION.SOUTH: 'cfg/s_configuration/s.sumo.cfg',
    DIRECTION.EAST: 'cfg/e_configuration/e.sumo.cfg',
}

MAX_STEPS = 360000  # 10000  # 1h = 360000
CONFIG_INDEX = 5
SAVE_PATH = 'testSave.xml'


def add_vehicle_fixed_route(step: int):
    route_id = "north_south"
    vid = "v.%s.%d" % (route_id, step)
    traci.vehicle.add(vid, route_id, typeID="vtypeauto")

    # route_id = "north_west"
    # vid = "v.%s.%d" % (route_id, step)
    # traci.vehicle.add(vid, route_id, typeID="vtypeauto")
    #
    # route_id = "north_east"
    # vid = "v.%s.%d" % (route_id, step)
    # traci.vehicle.add(vid, route_id, typeID="vtypeauto")

    # route_id = "south_west"
    # vid = "v.%s.%d" % (route_id, step)
    # traci.vehicle.add(vid, route_id, typeID="vtypeauto")


def add_vehicle_random(step: int):
    route_id = get_random_route()
    vid = "v.%s.%d" % (route_id, step)
    traci.vehicle.add(vid, route_id, typeID="vtypeauto")


def get_results_path():
    if not hasattr(get_results_path, "counter"):
        get_results_path.counter = 0
    if not hasattr(get_results_path, "current_time"):
        now = datetime.now()
        get_results_path.current_time = now.strftime("%H%M%S")
    if os.path.exists('results/' + get_results_path.current_time) is False:
        os.mkdir('results/' + get_results_path.current_time)

    path = 'results/%s/%s_%d_results.xml' % (get_results_path.current_time,
                                             get_results_path.current_time,
                                             get_results_path.counter)
    get_results_path.counter += 1
    return path


def get_sumo_cmd(is_gui=False):
    results_path = get_results_path()
    config = CONFIGURATIONS[DIRECTION.DEFAULT]
    if is_gui is True:
        return ['sumo-gui', '--duration-log.statistics', '--tripinfo-output', results_path, '-c', config]
    else:
        return ['sumo', '--duration-log.statistics', '--tripinfo-output', results_path, '-c', config]


def main():
    id_cnt = 0
    traffic_manager = Manager()

    for i in range(1):
        step_cnt = 0

        sumo_cmd = get_sumo_cmd(False)

        traci.start(sumo_cmd)

        if os.path.exists(SAVE_PATH):
            traci.simulation.loadState(SAVE_PATH)

        while step_cnt < MAX_STEPS:
            traci.simulationStep()
            traffic_manager.simulationStep(traci)

            step_cnt += 1

            if step_cnt > 2:
                # add_vehicle_random(step_cnt)
                add_vehicle_fixed_route(id_cnt)
                id_cnt += 1
        traci.simulation.saveState(SAVE_PATH)
        traci.close()

    if os.path.exists(SAVE_PATH):
        os.remove(SAVE_PATH)


if __name__ == "__main__":
    main()

'''
TODO:
1. Czy dobrze sumo przeskalowuje 100m na 1km. Wyliczylbym czy czas podrozy pojazdu jest prawidlowy.
Jezeli samochod jedzie 12m/s to powinien przebyc 1km w mniej niz 10s

2. Dodatkowy parametr w FuzzyDetector? Tj. Waiting Time.

3. Jak wchodze w 4 i 5 poziom kongestii - jaka jest srednia predkosc? Jaka jest gęstość?    
'''
