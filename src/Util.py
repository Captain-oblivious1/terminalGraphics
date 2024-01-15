from Model import *
from Point import *

_vToDArray = [ [ None          , Direction.UP  , None            ], \
               [ Direction.LEFT, Direction.NONE, Direction.RIGHT ], \
               [ None          , Direction.DOWN, None            ] ]

def vectorToDirection(vector):
    normed = vector.normalize().round()
    offset = normed + Point(1,1)
    return  _vToDArray[offset.y][offset.x]

def longestLineFor(text):
    longest,_ = longestLineAndNumberLines(text)
    return longest

def longestLineAndNumberLines(text):
    longest = 0
    current = 0
    nLines = 1
    for ch in text:
        if ch=='\n':
            nLines += 1
            if current>longest:
                longest = current
            current = 0
        else:
            current += 1
    if current>longest:
        longest = current

    return longest,nLines

