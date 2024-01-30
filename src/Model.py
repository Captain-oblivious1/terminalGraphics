from enum import Enum
import types

from Stroke import *

class Orientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1

class Element:
    def _attrToStr(self,attributeNames):
        result = ""
        first = True
        for attributeName in attributeNames:
            if first:
                first = False
            else:
                result+=","
            result += attributeName + "=" + str(getattr(self,attributeName))
        return result

    @staticmethod
    def _myFilter(attr):
        return not attr.startswith("_") and attr!="equals"

    def _genString(self,attributeNames):
        return self.__class__.__name__ + ":{" + self._attrToStr(attributeNames) + "}"

    def __str__(self):
        return self._genString(list(filter(lambda x: not x.startswith("_") and x!="isEqual", self.__dir__())))

class Diagram(Element):
    def __init__(self,name):
        Element.__init__(self)
        self.name = name
        self.elements = [] # front to back
        
    def isEqual(self,other):
        return \
            isEqual(self.name,other.name) and \
            isEqual(self.elements,other.elements)

class TextElement(Element):
    def __init__(self):
        super().__init__()
        self.text = None
        self.location = None
        self.justification = Justification.CENTER

    def isEqual(self,other):
        return \
            isEqual(self.text,other.text) and \
            isEqual(self.location,other.location) and \
            isEqual(self.justification,other.justification)

class Justification(Enum):
    LEFT = 0
    CENTER = 1
    RIGHT = 2

class Corners(Enum):
    SQUARE=0
    ROUND=1

class PathType(Enum):
    CLOSED = 0
    OPEN = 1

class Fill(Enum):
    OPAQUE = 0
    TRANSPARENT = 1

class PathElement(Element):
    def __init__(self):
        Element.__init__(self)
        self.startOrientation = 0
        self.turns = []
        self.corners = Corners.SQUARE
        self.pathType = PathType.CLOSED
        self.fill = Fill.TRANSPARENT
        self.style = Style.SOLID
        self.thickness = Thickness.THIN

    def isEqual(self,other):
        return isinstance(other,PathElement) and \
            isEqual(self.startOrientation,other.startOrientation) and \
            isEqual(self.turns,other.turns) and \
            isEqual(self.corners,other.corners) and \
            isEqual(self.pathType,other.pathType) and \
            isEqual(self.fill,other.fill) and \
            isEqual(self.style,other.style) and \
            isEqual(self.thickness,other.thickness)

class ShapeElement(PathElement):
    def __init__(self):
        PathElement.__init__(self)

    def isEqual(self,other):
        return isinstance(other,ShapeElement) and \
            super().isEqual(other)

class Direction(Enum):
    NONE = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    UP = 4

class Arrow(Enum):
    NONE = 0
    LINES = 1
    TRIANGLE = 2

class TableElement(Element):
    def __init__(self):
        self.location = None
        self.columnWidths = []
        self.rowHeights = []
        self.dataRows = []

    def isEqual(self,other):
        return isinstance(other,TableElement) and \
            isEqual(self.location,other.location) and \
            isEqual(self.columnWidths,other.columnWidths) and \
            isEqual(self.rowHeights,other.rowHeights) and \
            isEqual(self.dataRows,other.dataRows) 

class TableField:
    def __init__(self):
        self.justification = Justification.LEFT
        self.text = ''

    def isEqual(self,other):
        return isinstance(other,TableField) and \
            isEqual(self.justification,other.justification) and \
            isEqual(self.text,other.text)

class SequenceElement(Element):
    def __init__(self):
        self.top = None
        self.actors = []
        self.lines = []

    def isEqual(self,other):
        return isinstance(other,SequenceElement) and \
            isEqual(self.top,other.top) and \
            isEqual(self.actors,other.actors) and \
            isEqual(self.lines,other.lines)

class Actor:
    def __init__(self):
        self.x = None
        self.label = None

    def isEqual(self,other):
        return isinstance(other,Actor) and \
            isEqual(self.x,other.x) and \
            isEqual(self.label,other.label)

class Line:
    def __init__(self):
        self.y = None
        self.dashed = False
        self.fro = None
        self.to = None

    def isEqual(self,other):
        return isinstance(other,Line) and \
            isEqual(self.y,other.y) and \
            isEqual(self.dashed,other.dashed) and \
            isEqual(self.fro,other.fro) and \
            isEqual(self.to,other.to)

def isEqual(left,right):
    lType = type(left)
    if not lType is type(right):
        return False

    if lType==list:
        l = len(left)
        if l!=len(right):
            return False

        for i in range(l):
            if not isEqual(left[i],right[i]):
                return False

    elif hasattr(left,"isEqual"):
        if not left.isEqual(right):
            return False

    elif left!=right:
        return False

    return True
     
