from enum import Enum

GEO_DIRS = ('north', 'east', 'south', 'west')
CONFIGURATIONS = ('default', 'north', 'east', 'south', 'west')
DIRECTIONS = ('north_south', 'east_west', 'south_north', 'west_east')


class DIRECTION(Enum):
    DEFAULT = 0
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4
