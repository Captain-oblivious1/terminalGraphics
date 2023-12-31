from enum import Enum
import math

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

#class BoxElement(Element):
#    def __init__(self):
#        Element.__init__(self)
#        self.x = 0
#        self.y = 0
#        self.width = 0
#        self.height = 0

class Diagram(Element):
    def __init__(self):
        Element.__init__(self)
        self.name = ""
        self.elements = [] # front to back

class Justification(Enum):
    LEFT = 0
    CENTER = 1
    RIGHT = 2

#class LineOfText:
#    def __init__(self):
#        self.justification = Justification.LEFT
#        self.text = ""


#class TextBoxElement(BoxElement):
#    def __init__(self):
#        BoxElement.__init__(self)
#        self.lines = []
#
#    def autoFit(self):
#        self.width = 0
#        for line in self.lines:
#            lineLen = len(line.text)
#            if lineLen > self.width:
#                self.width = lineLen
#
#        self.width += 2 # For border on each side
#        self.height = len(self.lines) + 2 # for border on top and bottom

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

#class ConnectionPoint:
#    def __init__(self):
#        self.element = None
#        #self.side = None
#        self.segmentIndex = 0
#        self.where = None # 0.0 means left/top-most 1.0 is right/bottom most
#        self.end = Arrow.NONE

#class ConnectorElement(Element):
#    def __init__(self):
#        super().__init__()
#        self.fromConnection = None
#        self.toConnection = None
#        self.turns = [] # ints not actual points.
#
#def testTextBox():
#    textBox = TextBoxElement()
#
#    lineOfText = LineOfText()
#    lineOfText.text = "center"
#    lineOfText.justification = Justification.CENTER
#    textBox.lines.append(lineOfText)
#
#    lineOfText = LineOfText()
#    lineOfText.text = "How is life??"
#    lineOfText.justification = Justification.LEFT
#    textBox.lines.append(lineOfText)
#
#    lineOfText = LineOfText()
#    lineOfText.text = "right"
#    lineOfText.justification = Justification.RIGHT
#    textBox.lines.append(lineOfText)
#
#    lineOfText = LineOfText()
#    lineOfText.text = "left"
#    lineOfText.justification = Justification.LEFT
#    textBox.lines.append(lineOfText)
#
#    #textBox.isBold = True
#    textBox.autoFit()
#
#    print("textBox = " + str(textBox) )
#
#    return textBox
#
#def testDiagram():
#    diagram = Diagram()
#    diagram.width = 300
#    diagram.height = 200
#
#    diagram.elements.append( testTextBox() )
#
#    print("diagram = " + str(diagram) )


#testDiagram()
