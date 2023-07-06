from enum import Enum
import random

GEO_DIRS = ['north', 'east', 'south', 'west']
CONFIGURATIONS = ['default', 'north', 'east', 'south', 'west']
DIRECTIONS = ['north_south', 'east_west', 'south_north', 'west_east']


class DIRECTION(Enum):
    DEFAULT = 0
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4


def get_random_route() -> str:
    source = random.choice(GEO_DIRS)
    destination_list = GEO_DIRS
    destination_list.remove(source)
    destination = random.choice(destination_list)
    route = source + '_' + destination
    return route
