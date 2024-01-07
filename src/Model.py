from enum import Enum
import math

from Stroke import *

class Orientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1

class Element:
    def __init__(self):
        pass

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

    def _genString(self,attributeNames):
        return self.__class__.__name__ + ":{" + self._attrToStr(attributeNames) + "}"

    def __str__(self):
        return self._genString(list(filter(lambda x: not x.startswith("_"), self.__dir__())))

class TextElement(Element):
    def __init__(self):
        super().__init__()
        self.text = None
        self.location = None
        self.justification = Justification.CENTER

class Diagram(Element):
    def __init__(self,name):
        Element.__init__(self)
        self.name = name
        self.elements = [] # front to back

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

class ShapeElement(PathElement):
    def __init__(self):
        PathElement.__init__(self)


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
