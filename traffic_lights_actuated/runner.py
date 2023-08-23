import traci
import datetime
import argparse
import os

import sys
sys.path.append('C:\\Projects\\SUMO-SIMULATOR\\ReversibleLanesIntersection')
sys.path.append('C:\\Projects\\SUMO-SIMULATOR\\ReversibleLanesIntersection\\alda')
from TrafficGenerator import *
from utils import *

ROOT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


def get_results_path():
    if not hasattr(get_results_path, "counter"):
        get_results_path.counter = 0
    if not hasattr(get_results_path, "current_time"):
        now = datetime.datetime.now()
        get_results_path.current_time = now.strftime("%H%M%S")

    path = 'results/%s_%d_results.xml' % (get_results_path.current_time,
                                                        get_results_path.counter)
    result_path = os.path.join(ROOT_DIR, path)
    get_results_path.counter += 1
    return result_path


def main():
    parser = argparse.ArgumentParser(description='Simulator')
    parser.add_argument('--traffic', type=str, help='Path to output file.')
    args = parser.parse_args()

    if args.traffic:
        traffic = args.traffic
    else:
        traffic = "balanced"

    config = os.path.join(ROOT_DIR, "cfg/default_configuration/default.sumo.cfg")
    output_path = get_results_path()
    sumo_cmd = get_sumo_cmd(config, is_gui=False, results_path=output_path)
    traci.start(sumo_cmd, verbose=True)
    traffic_generator = TrafficGenerator(type=traffic)
    step_cnt = 0

    while step_cnt < MAX_STEPS:
        traci.simulationStep()
        traffic_generator.simulationStep(traci, step_cnt)

        step_cnt += 1

    if step_cnt >= MAX_STEPS:
        while traci.vehicle.getIDList():
            traci.simulationStep()
            step_cnt += 1
            print("step cnt:", step_cnt)

    traci.close()


if __name__ == "__main__":
    main()
