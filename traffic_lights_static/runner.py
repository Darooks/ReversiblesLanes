import traci
import time
import argparse

import sys
sys.path.append('C:\\Projects\\SUMO-SIMULATOR\\ReversibleLanesIntersection')
sys.path.append('C:\\Projects\\SUMO-SIMULATOR\\ReversibleLanesIntersection\\alda')
from TrafficGenerator import *
from utils import *
from alda.Manager import Manager

MAX_STEPS = 90000  # 10000  # 1h = 360000
SAVE_PATH = 'testSave.xml'


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


def main():
    parser = argparse.ArgumentParser(description='Simulator')
    parser.add_argument('--output_path', type=str, help='Path to output file.')
    args = parser.parse_args()

    if args.output_path:
        output_path = args.output_path
    else:
        output_path = get_results_path()

    sumo_cmd = get_sumo_cmd('cfg/default_configuration/default.sumo.cfg', is_gui=False, results_path=output_path)
    traci.start(sumo_cmd, verbose=True)
    traffic_generator = TrafficGenerator(type="balanced")
    step_cnt = 0

    while step_cnt < MAX_STEPS:
        traci.simulationStep()
        traffic_generator.simulationStep(traci, step_cnt)

        step_cnt += 1

    traci.close()


if __name__ == "__main__":
    main()
