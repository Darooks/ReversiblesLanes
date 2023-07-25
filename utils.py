from enum import Enum
from datetime import datetime
import os

GEO_DIRS = ('north', 'east', 'south', 'west')
CONFIGURATIONS = ('default', 'north', 'east', 'south', 'west')
DIRECTIONS = ('north_south', 'east_west', 'south_north', 'west_east')


class DIRECTION(Enum):
    DEFAULT = 0
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4


CONFIGURATIONS = {
    DIRECTION.DEFAULT.value: 'cfg/default_configuration/default.sumo.cfg',
    DIRECTION.NORTH.value: 'cfg/n_configuration/n.sumo.cfg',
    DIRECTION.WEST.value: 'cfg/w_configuration/w.sumo.cfg',
    DIRECTION.SOUTH.value: 'cfg/s_configuration/s.sumo.cfg',
    DIRECTION.EAST.value: 'cfg/e_configuration/e.sumo.cfg',
}


def get_sumo_cmd(config, is_gui=False, results_path=r"output/default_output.txt"):
    if is_gui is True:
        return ['sumo-gui', '--duration-log.statistics', '--tripinfo-output', results_path, '-c', config]
    else:
        return ['sumo', '--duration-log.statistics', '--tripinfo-output', results_path, '-c', config]