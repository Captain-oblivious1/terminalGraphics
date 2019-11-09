from enum import Enum

class Element:
    def __init__(self):
        self.parent = None

    def _attrToStr(self):
        return "parent=" + str(object.__str__(self.parent))

    def __str__(self):
        return "Element:{" + self._attrToStr() + "}"

class BoxElement(Element):
    def __init__(self):
        Element.__init__(self)
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0

    def _attrToStr(self):
        return Element._attrToStr() + ",x=" + str(self.x) + ",y=" + str(self.y) + ",width=" + str(self.width) + ",height=" + str(self.height)

    def __str__(self):
        return "BoxElement:{" + self._attrToStr() + "}"

class Diagram(Element):
    def __init__(self):
        Element.__init__(self)
        self.elements = [] # top to bottom (as in what in draw on top of what, not y locations)

    def _attrToStr(self):
        retMe = Element._attrToStr(self) + ",elements=["
        firstLine = True
        for element in self.elements:
            if firstLine:
                firstLine = False
            else:
                retMe += ","
            retMe += str(element)
        retMe += "]"
        return retMe

    def __str__(self):
        return "Diagram:{" + self._attrToStr() + "}"

class Justification(Enum):
    LEFT = 0
    CENTER = 1
    RIGHT = 2

class LineOfText:
    def __init__(self):
        self.justification = Justification.LEFT
        self.text = ""

    def _attrToStr(self):
        return "justification=" + str(self.justification) + ",text=\"" + self.text + "\""

    def __str__(self):
        return "LineOfText:{" + self._attrToStr() + "}"


class TextBoxElement(BoxElement):
    def __init__(self):
        BoxElement.__init__(self)
        self.lines = []

    def autoFit(self):
        self.width = 0
        for line in self.lines:
            lineLen = len(line.text)
            if lineLen > self.width:
                self.width = lineLen

        self.width += 2 # For border on each side
        self.height = len(self.lines) + 2 # for border on top and bottom

    def _attrToStr(self):
        retMe = Element._attrToStr(self) + ",lines=["
        firstLine = True
        for line in self.lines:
            if firstLine:
                firstLine = False
            else:
                retMe += ","
            retMe += str(line)
        retMe += "]"
        return retMe

    def __str__(self):
        return "TextBox:{" + self._attrToStr() + "}"

class Side(Enum):
    TOP = 0
    LEFT = 1
    RIGHT = 2
    BOTTOM = 3

class End(Enum):
    NONE = 0
    ARROW = 1
    TRIANGLE = 2

class ConnectionPoint:
    def __init__(self):
        self.element = None
        self.side = None
        self.where = None # 0.0 means left/top-most 1.0 is right/bottom most
        self.end = End.NONE


class ConnectorElement(Element):
    def __init__(self):
        Element.__init__(self)
        self.fromConnection = None
        self.toConnection = None
        self.controlPoints = [] # ints not actual points.

def testTextBox():
    textBox = TextBoxElement()

    lineOfText = LineOfText()
    lineOfText.text = "center"
    lineOfText.justification = Justification.CENTER
    textBox.lines.append(lineOfText)

    lineOfText = LineOfText()
    lineOfText.text = "How is life??"
    lineOfText.justification = Justification.LEFT
    textBox.lines.append(lineOfText)

    lineOfText = LineOfText()
    lineOfText.text = "right"
    lineOfText.justification = Justification.RIGHT
    textBox.lines.append(lineOfText)

    lineOfText = LineOfText()
    lineOfText.text = "left"
    lineOfText.justification = Justification.LEFT
    textBox.lines.append(lineOfText)

    #textBox.isBold = True
    textBox.autoFit()

    print("textBox = " + str(textBox) )

    return textBox

def testDiagram():
    diagram = Diagram()
    diagram.width = 300
    diagram.height = 200

    diagram.elements.append( testTextBox() )

    print("diagram = " + str(diagram) )


testDiagram()
