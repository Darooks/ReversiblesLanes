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

    is_gui = False
    verbose = True

    traffic_manager = Manager()
    traffic_generator = TrafficGenerator(type="balanced")
    is_cfg_changed = False
    step_cnt = 0

    start_time = time.time()

    while step_cnt < MAX_STEPS:
        curr_config = traffic_manager.get_config()
        sumo_cmd = get_sumo_cmd(curr_config, is_gui=is_gui, results_path=output_path)
        traci.start(sumo_cmd, verbose=True)

        if os.path.exists(SAVE_PATH):
            traci.simulation.loadState(SAVE_PATH)

        while step_cnt < MAX_STEPS:
            if is_cfg_changed is True:
                is_cfg_changed = False
                break

            traci.simulationStep()
            is_cfg_changed = traffic_manager.simulationStep(traci, verbose=verbose)
            traffic_generator.simulationStep(traci, step_cnt)

            step_cnt += 1
            if verbose is True:
                print("step_cnt:", step_cnt)
            else:
                n_bar = 50  # Progress bar width
                progress = step_cnt / MAX_STEPS
                curr_time = int(time.time() - start_time)
                sys.stdout.write('\r')
                sys.stdout.write(f"[{'=' * int(n_bar * progress):{n_bar}s}] {int(100 * progress)}%  {step_cnt}/{MAX_STEPS} {curr_time}s")
                sys.stdout.flush()
        traci.simulation.saveState(SAVE_PATH)
        traci.close()

    if os.path.exists(SAVE_PATH):
        os.remove(SAVE_PATH)


if __name__ == "__main__":
    main()
