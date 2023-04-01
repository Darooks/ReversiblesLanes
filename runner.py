import traci
from utils import *
from datetime import datetime
import os
from Manager import Manager

CONFIGURATIONS = {
    DIRECTION.NORTH: 'cfg/n_configuration/n.sumo.cfg',
    DIRECTION.WEST: 'cfg/w_configuration/w.sumo.cfg',
    DIRECTION.SOUTH: 'cfg/s_configuration/s.sumo.cfg',
    DIRECTION.EAST: 'cfg/e_configuration/e.sumo.cfg',
    DIRECTION.DEFAULT: 'cfg/default_configuration/default.sumo.cfg',
}

MAX_STEPS = 10000  # 1h = 360000
CONFIG_INDEX = 5
SAVE_PATH = 'testSave.xml'


def test_get_hc_route():
    if not hasattr(test_get_hc_route, "counter"):
        test_get_hc_route.counter = 0

    if test_get_hc_route.counter == 0:
        route = "north_south"
    else:
        route = "north_west"
    test_get_hc_route.counter += 1
    return route


def test_add_vehicle(veh_num: int):
    vid = "v.%d" % veh_num
    route_id = "north_east"  # test_get_hc_route()
    traci.vehicle.add(vid, route_id, typeID="vtypeauto")


def add_vehicle(step: int):
    vid = "v.%d" % step
    route_id = get_random_route()
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
    manager = Manager()

    for i in range(1):
        step_cnt = 0

        sumo_cmd = get_sumo_cmd()

        traci.start(sumo_cmd)
        # traci.lane.getLastStepVehicleNumber()

        if os.path.exists(SAVE_PATH):
            traci.simulation.loadState(SAVE_PATH)

        while step_cnt < MAX_STEPS:
            traci.simulationStep()
            manager.simulationStep(traci)

            step_cnt += 1

            if step_cnt > 2:
                # add_vehicle(step_cnt)
                test_add_vehicle(id_cnt)
                id_cnt += 1
        traci.simulation.saveState(SAVE_PATH)
        traci.close()

    if os.path.exists(SAVE_PATH):
        os.remove(SAVE_PATH)


if __name__ == "__main__":
    main()
