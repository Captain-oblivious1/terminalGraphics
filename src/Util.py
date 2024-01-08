from Model import *
from Point import *

_vToDArray = [ [ None          , Direction.UP  , None            ], \
               [ Direction.LEFT, Direction.NONE, Direction.RIGHT ], \
               [ None          , Direction.DOWN, None            ] ]

def vectorToDirection(vector):
    normed = vector.normalize().round()
    offset = normed + Point(1,1)
    return  _vToDArray[offset.y][offset.x]

