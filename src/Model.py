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
        return self._genString(list(filter(lambda x: not x.startswith("_") and x!="_isEqual", self.__dir__())))

class Diagram(Element):
    def __init__(self,name):
        Element.__init__(self)
        self.name = name
        self.elements = [] # front to back
        
    def _isEqual(self,other):
        return \
            _isEqual(self.name,other.name) and \
            _isEqual(self.elements,other.elements)

class TextElement(Element):
    def __init__(self):
        super().__init__()
        self.text = None
        self.location = None
        self.justification = Justification.CENTER

    def _isEqual(self,other):
        return \
            _isEqual(self.text,other.text) and \
            _isEqual(self.location,other.location) and \
            _isEqual(self.justification,other.justification)

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

    def _isEqual(self,other):
        return isinstance(other,PathElement) and \
            _isEqual(self.startOrientation,other.startOrientation) and \
            _isEqual(self.turns,other.turns) and \
            _isEqual(self.corners,other.corners) and \
            _isEqual(self.pathType,other.pathType) and \
            _isEqual(self.fill,other.fill) and \
            _isEqual(self.style,other.style) and \
            _isEqual(self.thickness,other.thickness)

class ShapeElement(PathElement):
    def __init__(self):
        PathElement.__init__(self)

    def _isEqual(self,other):
        return isinstance(other,ShapeElement) and \
            super()._isEqual(other)

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

    def _isEqual(self,other):
        return isinstance(other,TableElement) and \
            _isEqual(self.location,other.location) and \
            _isEqual(self.columnWidths,other.columnWidths) and \
            _isEqual(self.rowHeights,other.rowHeights) and \
            _isEqual(self.dataRows,other.dataRows) 

class TableField:
    def __init__(self):
        self.justification = Justification.LEFT
        self.text = ''

    def _isEqual(self,other):
        return isinstance(other,TableField) and \
            _isEqual(self.justification,other.justification) and \
            _isEqual(self.text,other.text)

class SequenceElement(Element):
    def __init__(self):
        self.top = None
        self.actors = []
        self.lines = []

    def _isEqual(self,other):
        return isinstance(other,SequenceElement) and \
            _isEqual(self.top,other.top) and \
            _isEqual(self.actors,other.actors) and \
            _isEqual(self.lines,other.lines)

class Actor:
    def __init__(self):
        self.x = None
        self.label = None

    def _isEqual(self,other):
        return isinstance(other,Actor) and \
            _isEqual(self.x,other.x) and \
            _isEqual(self.label,other.label)

class Line:
    def __init__(self):
        self.y = None
        self.dashed = False
        self.fro = None
        self.to = None
        self.text = "text"

    def _isEqual(self,other):
        return isinstance(other,Line) and \
            _isEqual(self.y,other.y) and \
            _isEqual(self.dashed,other.dashed) and \
            _isEqual(self.fro,other.fro) and \
            _isEqual(self.to,other.to) and \
            _isEqual(self.text,other.text) 

def _isEqual(left,right):
    lType = type(left)
    if not lType is type(right):
        return False

    if lType==list:
        l = len(left)
        if l!=len(right):
            return False

        for i in range(l):
            if not _isEqual(left[i],right[i]):
                return False

    elif hasattr(left,"_isEqual"):
        if not left._isEqual(right):
            return False

    elif left!=right:
        return False

    return True
     
