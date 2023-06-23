from enum import Enum
import random

GEO_DIRS = ['north', 'east', 'south', 'west']
CONFIGURATIONS = ['north', 'east', 'south', 'west', 'default']
DIRECTIONS = ['north_south', 'east_west', 'south_north', 'west_east']


class DIRECTION(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
    DEFAULT = 4


def get_random_route() -> str:
    source = random.choice(GEO_DIRS)
    destination_list = GEO_DIRS
    destination_list.remove(source)
    destination = random.choice(destination_list)
    route = source + '_' + destination
    return route
