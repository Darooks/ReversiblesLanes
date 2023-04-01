from enum import Enum
import random


class DIRECTION(Enum):
    NORTH = 0
    WEST = 1
    SOUTH = 2
    EAST = 3
    DEFAULT = 4


DIRECTIONS = ['north', 'east', 'south', 'west']


def get_random_route() -> str:
    source = random.choice(DIRECTIONS)
    destination_list = DIRECTIONS
    destination_list.remove(source)
    destination = random.choice(destination_list)
    route = source + '_' + destination
    return route
