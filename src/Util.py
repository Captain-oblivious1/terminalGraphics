from Model import *
from Point import *
from Rect import *

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
    if text=="":
        return 0,0

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


def rectForJustifiedText(x,y,text,justification):
    rect = Rect()
    executeLambdaForJustifiedText(x,y,text,justification, lambda x,y,text : rect.unionWith( Rect(x,y,len(text),1) ) )
    return rect

def executeLambdaForJustifiedText(x,y,text,justification,funct):
    lines = text.split('\n')

    if justification==Justification.LEFT:
        offsetCalc = lambda _ : 0
    else:
        if justification==Justification.RIGHT:
            offsetCalc = lambda t : -len(t)
        else:
            offsetCalc = lambda t : -int(len(t)/2)

    for i in range(len(lines)):
        funct(x+offsetCalc(lines[i]),y,lines[i])
        y += 1
