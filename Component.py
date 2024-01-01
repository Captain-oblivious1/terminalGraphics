from enum import Enum
from Model import *
from Rect import *
import math

def isHorizontal(side):
    return side == Direction.LEFT or side == Direction.RIGHT

class Component:
    def __init__(self, parent):
        self.parent = parent
        self.selected = False

    def getEditor(self):
        return self.parent.getEditor()

    def getRect(self):
        return Rect()

    def isSelected(self):
        return self.selected

    def setSelected(self,newSelected):
        self.selected = newSelected

    def children(self):
        return set()

    def isOnMe(self,point):
        return True  #this is only called if point is within bounding rect.

    def getTopLevelComponent(self):
        if self.parent==None:
            return self
        else:
            return self.parent.getTopLevelComponent()

    def getDiagramComponent(self):
        return self.getTopLevelComponent()

    def invalidate(self):
        self.getEditor().getContext().invalidateRect( self.getRect() )
